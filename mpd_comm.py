__author__ = 'peterb'

import serial
import datetime
from mpd import MPDClient

mopidyAddress = '192.168.13.13'
mopidyPort = 6600

client=MPDClient()
playlists={}

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
    playlists=client.listplaylists()

reconnect()

tracks=client.listplaylistinfo('schlafantonschlaf')

for t in tracks:
    print t['title']



