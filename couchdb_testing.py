__author__ = 'peterb'
import couchdb
import pickle


def delete_all_docs():
    view=(db.view('_all_docs',include_docs=True))
    if total_rows:
        for row in view:
            print row.doc
            db.delete(row.doc)

def add_phonebook(telefonBuch):
    for k in telefonBuch.keys():
         doc = telefonBuch[k]
         doc['number']=k
         doc['shuffle']=False
         db.save(doc)
         print k, telefonBuch[k]


def renew_database(telefonBuch):
    delete_all_docs()
    add_phonebook(telefonBuch)




fileName="/media/phonebook/phonebook"
telefonBuch=pickle.load( open( fileName+'.pkl', "rb" ) )




server = couchdb.Server()
import time
print time.time()
for db in server:
    print db

db = server['test']


#renew_database(telefonBuch)

view=(db.view('_design/playlists/_view/numbers'))
if view.total_rows:
    numbers = {row.key:row.id for row in view}

print view.total_rows
print numbers


for k in telefonBuch.keys():

    doc = telefonBuch[k]
    if k in numbers.keys():
        doc_couch = db[numbers[k]]
        doc['shuffle']='whatever'
        for doc_key in doc.keys():
            doc_couch[doc_key]=doc[doc_key]
        db.save(doc_couch)

    else:
        doc['number']=k
        doc['shuffle']=False
        db.save(doc)
        print k, telefonBuch[k]


view=(db.view('_design/playlists/_view/numbers'))
print view.total_rows

# #
# #
# # #
#
# view=(db.view('_design/numbers/_view/numbers'))
# for row in view:
#     print row.key