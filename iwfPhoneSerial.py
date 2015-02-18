#!/root/PhoneBookProject/venv/bin/python
# -*- coding: utf-8 -*-

__author__ = 'peterb'

import serial
import datetime
from mpd import MPDClient
import urllib2

mopidyAddress = '192.168.13.13'
mopidyPort = 6600

client=MPDClient()

def reconnect():
    global client
    global playlists
    try:
        client.disconnect()
    except:
        pass
    client.timeout = 10
    client.idletimeout = None
    client.connect(mopidyAddress,mopidyPort)
    client.password('IlPits2013')


def get_USBPort_name():
    name=None
    for i in range(200):
        try:
            ser=serial.Serial('/dev/ttyAMA%i'%i,115200,timeout=1)
            name=ser.name
            ser.close()
            break
        except:
            pass
    return name


def initSerialPort(name):
    ser=serial.Serial(name,115200,timeout=1)
    return ser


def getVol():

    stat=client.status()
    vol=int(stat['volume'])
    return vol


def play_by_number(number):
    #try:
        resp=urllib2.urlopen('http://192.168.13.13:8080/play_number/%i'%number)
        name=resp.readline()
        print(number,name)
    #except:
    #    pass


#play_by_number(3)

serialName=get_USBPort_name()
if serialName:
    ser=initSerialPort(serialName)




reconnect()
connectTime=datetime.datetime.now()


actionTime=False
lastAction=datetime.datetime.now()
actionTimestamp=0


LOST_ACTION_TIME=10
vol=getVol()


last_number_time=datetime.datetime.now()
dail_timeout=3
number=0
newDail=False


while True:
    if not(actionTime):
        vol=getVol()
    if (datetime.datetime.now()-lastAction).total_seconds()>LOST_ACTION_TIME:
        actionTime=False
    try:
        line=ser.readline()
        line=line.decode()
        line=line.strip()
    except:
        print('serial read error')

    
    if line!="":
        print(line)
        if line.split('.')[0]=='rot':
            dir=line.split('.')[1]
            actionTime=True
            lastAction=datetime.datetime.now()

            if dir=="+" or dir=="-":
                if dir=="+":
                    changeVol=+5
                elif dir=="-":
                    changeVol=-5
                vol=vol+changeVol
                try:
                    client.setvol(vol)
                except:
                    print('setting volume failed')
            elif dir=="p":
                try:
                    client.pause()
                except:
                    print('pause failed')
            elif dir=="h":
                try:
                    client.seekcur(0)
                except:
                    print('backseek failed')
            elif dir=="d":
                try:
                    client.next()
                except:
                    print('next failed')



        if line.split('.')[0]=='tel':
            try:
                new_number=line.split('.')[1]
                new_number=int(new_number)
                last_number_time=datetime.datetime.now()
                number=number*10+new_number
                print(number)
                newDail=True
            except:
                print(line)


    if newDail and ((datetime.datetime.now()-last_number_time).total_seconds()>dail_timeout):
        print('play number%s'%number)
        play_by_number(number)
        number=0
        newDail=False

    if (datetime.datetime.now()-connectTime).total_seconds()>99:
        try:
            print('reconnect')
            reconnect()
            client.clearerror()
        except:
            pass
        connectTime=datetime.datetime.now()
        

ser.close()

