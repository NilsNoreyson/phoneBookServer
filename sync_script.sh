rsync -rav root@192.168.13.13:/media/phonebook /media/
rsync -rav --delete root@192.168.13.13:/media/playlists /media/

rsync -rvl --delete --files-from=/media/satellite_mpds/files2sync.txt /media/music /media/satellite_mpds/music

rsync -rav root@192.168.13.13:/media/phonebook /media/satellite_mpds/
rsync -rav root@192.168.13.13:/media/playlists /media/satellite_mpds/


