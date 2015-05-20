import sys

reload(sys)
sys.setdefaultencoding('utf8')

from mpd import MPDClient

import pickle
fileName="/opt/phonebook/phonebook"

def load_phoneBook():
    telefonBuch=pickle.load( open( fileName+'.pkl', "rb" ) )
    testKey=telefonBuch.keys()[0]
    for k in telefonBuch.keys():
        if isinstance(telefonBuch[k],dict):
            pass
        else:
            telefonBuch[k]={'name':telefonBuch[k]}

    return telefonBuch


def play_playlist(name):
    client=MPDClient()
    mopidyAddress = 'localhost'
    mopidyPort = 6600

    client.timeout = 10
    client.idletimeout = None
    client.connect(mopidyAddress,mopidyPort)
    #client.password('IlPits2013')
    client.clear()
    if playlist_exists(name):
        client.load(name)
    spotify_lists = get_spotify_playlists()
    name = name.encode('utf-8')
    print name
    #print spotify_lists
    if name in spotify_lists:
        add_spotify_directory(name)
    #time.sleep(1)
    if name == 'Pierre':
        client.shuffle()

    #client.setvol(50)
    #client.play()
    client.disconnect()
    return

def playlist_exists(name):
    client=MPDClient()
    mopidyAddress = 'localhost'
    mopidyPort = 6600

    client.timeout = 10
    client.idletimeout = None
    client.connect(mopidyAddress,mopidyPort)
    #client.password('IlPits2013')

    playlists = client.listplaylists()

    p_names = [p['playlist'] for p in playlists]

    client.disconnect()
    return name in p_names


def get_spotify_playlists():
    client=MPDClient()
    mopidyAddress = '192.168.13.13'
    mopidyPort = 6600

    client.timeout = 10
    client.idletimeout = None
    client.connect(mopidyAddress,mopidyPort)
    client.password('IlPits2013')
    folders = client.listall('Spotify')
    #folders = client.lsinfo('Spotify')
    folders = [f['directory'].split(r'/')[1] for f in folders if 'directory' in f.keys()]
    #folders = [f['directory'].split(r'/') for f in folders if 'directory' in f.keys()]
    #folders = [f[1] for f in folders if len(f)==2]
    client.disconnect()
    return folders

def add_spotify_directory(name):
    client=MPDClient()
    mopidyAddress = 'localhost'
    mopidyPort = 6600

    client.timeout = 10
    client.idletimeout = None
    client.connect(mopidyAddress,mopidyPort)
    #client.password('IlPits2013')
    foldername = 'Spotify/{name:s}'.format(name=name)

    files = client.lsinfo(foldername)
    files = [x['file'] for x in files]
    files = sorted(files)
    for f in files:
        client.add(f)
    #print(files)
    client.disconnect()


def print_files():
    sync_files = open('sync_files.txt','w')
    client=MPDClient()
    mopidyAddress = 'localhost'
    mopidyPort = 6600

    client.timeout = 10
    client.idletimeout = None
    client.connect(mopidyAddress,mopidyPort)
    #client.password('IlPits2013')
    files = client.playlistinfo()
#    files = client.lsinfo(foldername)
    files = [x['file'] for x in files]
    files = sorted(files)
    for f in files:
        sync_files.write(f+'\n')
        print f
    sync_files.close()
    #print(files)
    client.disconnect()



phone_book = load_phoneBook()

for entry in phone_book.values():
    play_playlist(entry['name'])
    print_files()

