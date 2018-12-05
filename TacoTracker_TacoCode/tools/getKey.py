#!/usr/bin/env python3

key = 'E2bywHLZ7M0bCGoh587KW7lX7Zc'
shift = 64
buf = ''
for x in key:
    buf += '\\x%02x' % ((ord(x) - shift) & 0xff)
print buf
