# -*- coding: utf-8 -*-

__author__ = 'peterb'

import serial
import datetime
from mpd import MPDClient
from flask import Flask,jsonify
import time

def get_playlists_from_mpd():
    client=MPDClient()
    mopidyAddress = '192.168.13.13'
    mopidyPort = 6600

    client.timeout = 10
    client.idletimeout = None
    client.connect(mopidyAddress,mopidyPort)
    client.password('IlPits2013')

    playlists=client.listplaylists()
    playlist_names=[p['playlist'] for p in playlists]

    spotify_playlists = get_spotify_playlists()
    playlists = playlist_names+spotify_playlists
    client.disconnect()
    return playlists

def play_playlist(name):
    client=MPDClient()
    mopidyAddress = '192.168.13.13'
    mopidyPort = 6600

    client.timeout = 10
    client.idletimeout = None
    client.connect(mopidyAddress,mopidyPort)
    client.password('IlPits2013')
    client.clear()
    if playlist_exists(name):
        client.load(name)
    spotify_lists = get_spotify_playlists()
    name = name.encode('utf-8')
    print name
    print spotify_lists
    if name in spotify_lists:
        add_spotify_directory(name)
    time.sleep(1)
    if name == 'Pierre':
        client.shuffle()

    #client.setvol(50)    
    client.play()
    client.disconnect()
    return

def playlist_exists(name):
    client=MPDClient()
    mopidyAddress = '192.168.13.13'
    mopidyPort = 6600

    client.timeout = 10
    client.idletimeout = None
    client.connect(mopidyAddress,mopidyPort)
    client.password('IlPits2013')

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
    mopidyAddress = '192.168.13.13'
    mopidyPort = 6600

    client.timeout = 10
    client.idletimeout = None
    client.connect(mopidyAddress,mopidyPort)
    client.password('IlPits2013')
    foldername = 'Spotify/{name:s}'.format(name=name)

    files = client.lsinfo(foldername)
    files = [x['file'] for x in files]
    files = sorted(files)
    for f in files:
        client.add(f)
    #print(files)
    client.disconnect()


if __name__=='__main__':

    #playlists=get_playlists_from_mpd()
    #print playlists
    #print('test' in playlists)
    folders = get_spotify_playlists()
    #print(folders)
    #add_spotify_directory('Pierre')
    #load_playlist(just_namelist[7])
    # tracks=client.listplaylistinfo('schlafantonschlaf')
    #
    # for t in tracks:
    #     print t['title']
    #play_playlist('Pierre')
    print get_spotify_playlists()

