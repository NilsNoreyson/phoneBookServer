__author__ = 'peterb'

#!/root/PhoneBookProject/venv/bin/python

__author__ = 'peterb'

import datetime
from mpd import MPDClient
#import urllib2

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

reconnect()
print(client.volume(1))
#client.set_vol(1)