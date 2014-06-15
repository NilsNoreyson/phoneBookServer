# -*- coding: utf-8 -*-
"""
Created on Tue May 13 14:28:23 2014

@author: peterb
"""

from flask import Flask,jsonify,request, make_response
#from relatorio.templates.opendocument import Template
import os
#from createLetterData import *

import tempfile
topPath=os.path.dirname(os.path.realpath(__file__))

# from OpenSSL import SSL
# context = SSL.Context(SSL.SSLv23_METHOD)
# context.use_privatekey_file(os.path.join(topPath,'ssl/server.key'))
# context.use_certificate_file(os.path.join(topPath,'ssl/server.crt'))



app = Flask(__name__, static_url_path='')

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/createLetter',methods=['POST'])
def createLetter():
    
#    if request.form:
#        data={'recipient':json.loads(request.form['recipient']),
#              'sender':json.loads(request.form['sender'])}
#    elif (request.json):
#        data=request.json
#    
    data={'recipient':json.loads(request.form['recipient']),
              'sender':json.loads(request.form['sender'])}    
    
    letter_data=jsonToLetterData(data)
    print letter_data

    basic = Template(source="IPC_DATA", filepath=os.path.join(topPath,'IPC_ger_Letter.odt'))
    print('TemplateDone')
    basic_generated = basic.generate(o=letter_data).render()
    print('filled Done')
    odt_data=basic_generated.getvalue()
    print('generated Done')
    
    f = tempfile.NamedTemporaryFile(delete=False,mode='wb',dir=os.path.join(topPath,'static'))
    print("%s.odt"%f.name)
    
    f.write(odt_data)
    
    response=make_response(odt_data)
    fileRecipientFirst=letter_data['recipient']['surname'].encode('ascii','ignore')
    fileRecipientSur=letter_data['recipient']['firstname'].encode('ascii','ignore')
    fileDate=letter_data['date']
    filename="Letter_to_%s_%s_%s"%(fileRecipientFirst,fileRecipientSur,fileDate)
    response.headers["Content-Disposition"] = "attachment; filename=%s.odt"%filename
    response.mimetype='text/odt'
    
    return response
    
    #return jsonify({'status': 'OK','filename':os.path.basename(f.name)})


@app.route('/download/<filename>')
def download(filename):
    filename=os.path.join(topPath,'static',filename)
    f=open(filename,'rb')
    odt_data=f.read()
    
    response=make_response(odt_data)
    
    response.headers["Content-Disposition"] = "attachment; filename=Letter.odt"
    
    return response



    
if __name__ == '__main__':
    #app.run(host='0.0.0.0',port=443,ssl_context=context,debug=True)
    app.run(host='0.0.0.0',port=8080,debug=True)
