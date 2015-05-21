#!/bin/bash
rsync -avz --delete -e ssh treize@treize.duckdns.org:/media/satellite_mpds/music/ /media/music
rsync -avz --delete -e ssh treize@treize.duckdns:/media/satellite_mpds/phonebook/ /media/phonebook
rsync -avz --delete -e ssh treize@treize.duckdns:/media/satellite_mpds/playlists/ /media/playlists

mkdir /media/mpd
chown -R mpd:mpd /media/
mpc update 

