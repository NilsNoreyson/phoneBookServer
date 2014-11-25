#!/root/PhoneBookProject/venv/bin/python

# -*- coding: utf-8 -*-
"""
Created on Tue May 13 14:28:23 2014

@author: peterb
"""


from flask import Flask,jsonify,request, make_response
import os
from mpd_comm import *
import json
import threading
import pickle
import datetime

fileName="/opt/phonebook/phonebook"

telefonBuch={9: 'Toystore',
             3: 'anton',
             1: 'Stan',
             7: 'Kalkbrenner',
             2: 'Hit Box',
             4: 'The Katie Melua Collection',
             6: 'IRM',
             5: 'Anthems of All',
             8: 'Broken Bells',
             0: 'Another Self Portrait',
             145:'Extrawelt',
             333:'Streets',

            }
playlists=[]

def save_to_pickle():
    pickle.dump(telefonBuch, open( fileName+'.pkl', "wb" ) )
    date_str=datetime.datetime.now().strftime('%Y-%m-%d_%H-%M')
    pickle.dump(telefonBuch, open( fileName+"_"+date_str+'_.pkl', "wb" ) )
    return


def load_phoneBook():
    telefonBuch=pickle.load( open( fileName+'.pkl', "rb" ) )
    testKey=telefonBuch.keys()[0]
    for k in telefonBuch.keys():
        if isinstance(telefonBuch[k],dict):
            pass
    else:
        telefonBuch[k]={'name':telefonBuch[k]}
        
    return telefonBuch


#save_to_pickle()
telefonBuch=load_phoneBook()
print(telefonBuch)

topPath=os.path.dirname(os.path.realpath(__file__))


app = Flask(__name__, static_url_path='')




@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/get_phonebook')
def get_telefonBuch():
    return "".join(["%i - %s<br/>"%(k,telefonBuch[k]['name']) for k in sorted(telefonBuch.keys())])

    return jsonify(telefonBuch)

@app.route('/remove_number/<number>')
def remove_number(number):
    try:
        number=int(number)
        if telefonBuch.has_key(number):
            telefonBuch.pop(number,0)
        else:
            pass
    except:
        pass

    return app.send_static_file('index.html')



@app.route('/set_number',methods=['POST'])
def set_number():
    try:
        name=request.form['playlist_input']
        number=int(request.form['number_input'])
        #shuffle=request.form['shuffle']
        print number,name
        #print shuffle

        telefonBuch[number]={'name':name}
        save_to_pickle()
    except:
        print('set fail')
        pass
    return app.send_static_file('index.html')


@app.route('/play_number/<number>')
def play_number(number):
        number=int(number)
        if telefonBuch.has_key(number):
            name=telefonBuch[number]
            name=name.encode('utf-8',errors='ignore')
            print name
            print number
            try:
                play_playlist(name)
            except:
                return('play fail')
                pass
            return name

@app.route('/get_playlists')
def get_playlists():
    global playlists
    try:
        just_namelist=get_playlists_from_mpd()
    except:
        pass

    #print(just_namelist)
    return json.dumps(just_namelist)


if __name__ == '__main__':
    #app.run(host='0.0.0.0',port=443,ssl_context=context,debug=True)
    app.run(host='0.0.0.0',port=8080,debug=True)
