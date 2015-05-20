__author__ = 'peterb'

from Flask2 import *

print(telefonBuch)

play_number(123)

client=MPDClient()
mopidyAddress = '192.168.13.13'
mopidyPort = 6600

client.timeout = 10
client.idletimeout = None
client.connect(mopidyAddress,mopidyPort)
client.password('IlPits2013')
playlist = client.playlistinfo()

for p in playlist:
    print(p['file'])

client.disconnect()