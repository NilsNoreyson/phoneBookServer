__author__ = 'peterb'

import simplejson
import json
import urllib2

phoneBook=json.loads((urllib2.urlopen("http://localhost:8080").read()))

phoneBook=dict((int(key), value.encode()) for (key, value) in phoneBook.items())

print(phoneBook)

