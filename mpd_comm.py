# -*- coding: utf-8 -*-

__author__ = 'peterb'

import serial
import datetime
from mpd import MPDClient
from flask import Flask,jsonify
import time
import os

def get_connected(addr = '192.168.13.50', port = 6642, password = None):
    client=MPDClient()
    mopidyAddress = addr
    mopidyPort = port

    client.timeout = 10
    client.idletimeout = None
    client.connect(mopidyAddress,mopidyPort)
    if password:
        client.password('IlPits2013')
    return client


def get_playlists_from_mpd():
    client=get_connected()

    playlists=client.listplaylists()
    folder_above = [{'name':'..','parent':'','above': '', 'full':'', 'action_type':None}]
    playlist_names=[p['playlist'] for p in playlists]

    playlists = folder_above + [{'name':p,'parent':'Playlists','above':'', 'full':p, 'action_type':'load'} for p in playlist_names]


    client.disconnect()
    return playlists

def play_playlist(name):
    client=get_connected()
    client.clear()

    if playlist_exists(name):
        client.load(name)
    # spotify_lists = get_spotify_playlists()
    # name = name.encode('utf-8')
    # print name
    # print spotify_lists
    # if name in spotify_lists:
    #     add_spotify_directory(name)
    time.sleep(1)
    if name == 'Pierre':
        client.shuffle()

    #client.setvol(50)    
    client.play()
    client.disconnect()
    return

def playlist_exists(name):
    client=get_connected()

    playlists = client.listplaylists()

    p_names = [p['playlist'] for p in playlists]

    client.disconnect()
    return name in p_names


def get_folder_from_mpd(folder=''):
    print folder
    if folder=='':
        folders = [{'name':'..','parent':'','above': '', 'full':''},{'name':'Playlists','parent':'','above': '','action_type':None, 'full':'Playlists'}, {'name':'Folders','parent':'','above': '', 'action_type':None, 'full':'Folders'}]
        return folders
    elif folder=='Folders':
        parent_folder = ''
        folder=''
    elif folder == 'Playlists':
        return get_playlists_from_mpd()

    else:
        parent_folder = os.path.dirname(folder)



    client=get_connected()

    folders = client.lsinfo(folder)
    print folders
    #folders = client.lsinfo('Spotify')
    #
    dict_names = [f['directory'] for f in folders if 'directory' in f.keys()]
    file_names = [f['file'] for f in folders if 'file' in f.keys()]
    all_data = dict_names+file_names
    print folders
    folder_above = [{'name':'..','parent':parent_folder,'above': parent_folder, 'full':parent_folder, 'action_type':None}]

    folders_names = [{'name':os.path.basename(f),'parent':os.path.dirname(f),'above':os.path.dirname(os.path.dirname(f)), 'full':f, 'action_type':'add'} for f in all_data]

    if folders_names:
        folder_above.extend(folders_names)




    client.disconnect()

    return folder_above



def get_spotify_playlists():
    client=get_connected()

    #folders = client.listall('Spotify') ##old way no mopidy
    #folders = client.listall('Files/Spotify')
    folders = client.lsinfo('Files/Spotify')
    print folders
    #folders = [f['directory'].split(r'/')[1] for f in folders if 'directory' in f.keys()] #old way no mopidy
    folders = [f['directory'].split(r'/')[2] for f in folders if 'directory' in f.keys()]
    #folders = [f['directory'].split(r'/') for f in folders if 'directory' in f.keys()]
    #folders = [f[1] for f in folders if len(f)==2]
    client.disconnect()
    return folders

def add_spotify_directory(name):
    client=get_connected()

    foldername = 'Spotify/{name:s}'.format(name=name) ##old way without mopidy
    foldername = 'Files/Spotify/{name:s}'.format(name=name)
    print foldername
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
    play_playlist('00-13')
    print get_spotify_playlists()

