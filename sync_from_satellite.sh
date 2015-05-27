#!/bin/bash
ssh_port=2213
rsync -avz --delete -e "ssh -p $ssh_port" treize@treize.duckdns.org:/media/satellite_mpds/music/ /media/music
rsync -avz --delete -e "ssh -p $ssh_port" treize@treize.duckdns.org:/media/satellite_mpds/phonebook/ /media/phonebook
rsync -avz --delete -e "ssh -p $ssh_port" treize@treize.duckdns.org:/media/satellite_mpds/playlists/ /media/playlists

mkdir /media/mpd
chown -R mpd:mpd /media/
mpc update 
systemctl restart telFlask
