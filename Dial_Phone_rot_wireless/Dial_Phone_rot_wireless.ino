#include <RFduinoGZLL.h>
device_t role = DEVICE0;

#define INCREASE_VOLUME "rot.+"
#define DECREASE_VOLUME "rot.-"
#define SINGLE_BUTTON "rot.p"
#define DOUBLE_BUTTON "rot.d"
#define HOLD_BUTTON "rot.h"

#define PIN_HIGHBIT (6)
#define PIN_LOWBIT  (5)
#define BUTTON (4)

#define BAUD    (115200)

#define VOLUME_CHANGE_DELAY (70)
#define BUTTON_HOLD_TIME (800)
#define BUTTON_DEBOUNCE (30)
#define BUTTON_DOUBLE_CLICK_MAX (350)
#define TIME_BEFORE_SLEEP (3000)
#define SLEEP_TIME_CONNECTED (300)
#define SLEEP_TIME_DISCONNECTED (200)


// globals
int state, prevState = 0;
/* old state, new state, change (+ means clockwise)
 * 0 2 +
 * 1 0 +
 * 2 3 +
 * 3 1 +
 * 0 1 -
 * 1 3 -
 * 2 0 -
 * 3 2 -
 */
int encoderStates[4][4] = {
 {  0, -1,  1,  0 }, 
 {  1,  0,  0, -1 }, 
 { -1,  0,  0,  1 }, 
 {  0,  1, -1,  0 }, 
};



unsigned long lastVolumeAdjust = 0;
unsigned long lastButtonPress = 0;
int sleepTime = SLEEP_TIME_DISCONNECTED;



//for the dialing phone
int dialPin = 2; // GPIO für Messung am Telefon
int dialVal = 0;
int dialValStat = 1;

int nummer = 0;
int taste = 10;

unsigned long int signalstart = 0;
unsigned long int signalstop = 0;

unsigned long int signalzeit = 0;
unsigned long int keinsignalzeit = 0;

unsigned long int auszeit = 200;
unsigned long int zwischenzeit = 600;

int midValue = 1000; // der Schwellenwert um aufgelegt (LOW) von abgenommen (HIGH) zu unterscheiden

boolean dialing = false;
boolean aufgelegt = false;

//GZLL send string
String stringToSend;
char tasten[11] = "0123456789";


void setup(){
  RFduinoGZLL.begin(role);
  
  //rotary encoder stuff
  pinMode(PIN_HIGHBIT, INPUT_PULLUP);
  pinMode(PIN_LOWBIT, INPUT_PULLUP);
  pinMode(BUTTON, INPUT_PULLUP);
  RFduino_pinWake(BUTTON, LOW);
  RFduino_pinWake(PIN_HIGHBIT, LOW);
  RFduino_pinWake(PIN_LOWBIT, LOW);
  
  //phone stuff
  pinMode(dialPin, INPUT_PULLUP);
  RFduino_pinWake(dialPin, HIGH);
  
  Serial.begin(BAUD);
}



void loop(){
  checkButton();
  adjustVolume();
  check_phone();
    
  if((millis() - lastVolumeAdjust > TIME_BEFORE_SLEEP) && (millis() - lastButtonPress > TIME_BEFORE_SLEEP) && nummer==0 && false){
    //Serial.println("sleeping");
    //RFduinoGZLL.sendToHost("tel.sleepy");
    delay(100);
    //RFduino_ULPDelay(sleepTime);
    if(RFduino_pinWoke(BUTTON)){
      RFduino_resetPinWake(BUTTON);
    }
    if(RFduino_pinWoke(PIN_HIGHBIT)){
      RFduino_resetPinWake(PIN_HIGHBIT);
    }
    if(RFduino_pinWoke(PIN_LOWBIT)){
      RFduino_resetPinWake(PIN_LOWBIT);
    }
    if(RFduino_pinWoke(dialPin)){
      RFduino_resetPinWake(dialPin);
    }

   RFduino_ULPDelay(INFINITE);
   //Serial.println("wake");
   //RFduinoGZLL.sendToHost("tel.wokeup");
 
  } 
}



void adjustVolume(){
  state = (digitalRead(PIN_HIGHBIT) << 1) | digitalRead(PIN_LOWBIT);
  int value = encoderStates[prevState][state];
  
  if(state != prevState){
    unsigned long elapsedSinceVolumeChange = millis() - lastVolumeAdjust;
    if(elapsedSinceVolumeChange >= VOLUME_CHANGE_DELAY){
      if(value == -1){
        Serial.print(DECREASE_VOLUME);
        RFduinoGZLL.sendToHost(DECREASE_VOLUME);
        lastVolumeAdjust = millis();
      }
      else if(value == 1){
        Serial.print(INCREASE_VOLUME);
        RFduinoGZLL.sendToHost(INCREASE_VOLUME);
        lastVolumeAdjust = millis();
      }
    }
  }
  prevState = state;
}




void checkButton(){
  boolean buttonDown = (digitalRead(BUTTON) == LOW);
  
  if(buttonDown){
    unsigned long buttonDownStartTime = millis();
    delay(BUTTON_DEBOUNCE);
    
    while(digitalRead(BUTTON) == LOW){
      if(millis()-buttonDownStartTime >= BUTTON_HOLD_TIME){
        //RFduinoBLE.sendByte(HOLD_BUTTON);
        Serial.println(HOLD_BUTTON);
        RFduinoGZLL.sendToHost(HOLD_BUTTON);
        break;
      }
    }
    
    delay(BUTTON_DEBOUNCE);

    if(digitalRead(BUTTON) == HIGH){
       unsigned long buttonUpStartTime = millis();
       delay(BUTTON_DEBOUNCE);
       while(digitalRead(BUTTON) == HIGH){
         if(millis() - buttonUpStartTime > BUTTON_DOUBLE_CLICK_MAX){
          //RFduinoBLE.sendByte(SINGLE_BUTTON);
          //Serial.println(SINGLE_BUTTON);
          RFduinoGZLL.sendToHost(SINGLE_BUTTON);
          break;
         }
       }
       delay(BUTTON_DEBOUNCE);
       if(digitalRead(BUTTON) == LOW){
         //RFduinoBLE.sendByte(DOUBLE_BUTTON);
         
         Serial.println(DOUBLE_BUTTON);
         RFduinoGZLL.sendToHost(DOUBLE_BUTTON);
       }
    }
    
    while(digitalRead(BUTTON) == LOW){}
    lastButtonPress = millis();
    delay(BUTTON_DEBOUNCE);
  }
  
}


//telefon funktionen

void check_phone()
{

  if (digitalRead(dialPin)==HIGH)
  {
    dialVal = 1;
  } else {
    dialVal = 0;
  }

 
  if ( dialVal != dialValStat )
  {
    dialValStat = dialVal;
    //Serial.println("AHHHH");
    if (dialVal == HIGH)
    {
      signalstop = millis();
      nummer++;
      Serial.println("tel.dialing");
      //RFduinoGZLL.sendToHost("dial");
      delay(100);

    }
  }

  /*
  *   Abfrage ob waehlscheibe runtergelaufen
  */
  keinsignalzeit = millis() - signalstop;

  if ( keinsignalzeit > zwischenzeit )
  {
    if (nummer == 10) 
    {
      taste = 0;
    } 
    else if (nummer > 0) {
      taste = nummer;
    }
    if (taste < 10) 
    {
      Serial.print("tel.");
      Serial.print(taste);
      Serial.println();
      
      stringToSend = String("tel.");
      stringToSend.concat(taste);
      RFduinoGZLL.sendToHost(stringToSend);
      //RFduinoGZLL.sendToHost(tasten[taste]);
    }

    nummer = 0;
    taste = 10;
  }


  /*
  *   abfrage ob hoerer aufgelegt
   */
  
}

