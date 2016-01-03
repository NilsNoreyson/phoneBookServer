#!/root/PhoneBookProject/venv/bin/python
# -*- coding: utf-8 -*-

__author__ = 'peterb'

import serial
import datetime
from mpd import MPDClient
import urllib2
from ble_phone import BTLE_PHONE
import time


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


mopidyAddress = '192.168.13.13'
mopidyPort = 6600

client=MPDClient()
ble = BTLE_PHONE('EE:A7:8B:BB:45:D4')



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

vals_old = []
vals = None
while True:
    #time.sleep(0.1)
    if not(actionTime):
        vol=getVol()
    if (datetime.datetime.now()-lastAction).total_seconds()>LOST_ACTION_TIME:
        actionTime=False

    vals = ble.get_last_command()

    if vals and len(vals)==3:
        print 'vals',vals
        if vals[0]==2:
            actionTime=True
            lastAction=datetime.datetime.now()

            if vals[1]==1 or vals[1]==0:
                if vals[1]==1:
                    changeVol=+2
                elif vals[1]==0:
                    changeVol=-2
                vol=vol+changeVol
                try:
                    client.setvol(vol)
                except:
                    print('setting volume failed')
        if vals[0]==1:
            if vals[1]==0:
                try:
                    client.pause()
                except:
                    print('pause failed')
            elif vals[1]==1:
                try:
                    client.seekcur(0)
                except:
                    print('backseek failed')
            elif vals[1]==2:
                try:
                    client.next()
                except:
                    print('next failed')



        if vals[0]==3:
            new_number=vals[1]
            new_number=int(new_number)
            last_number_time=datetime.datetime.now()
            number=number*10+new_number
            print(number)
            newDail=True



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
        



