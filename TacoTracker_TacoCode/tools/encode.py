#!/usr/bin/env python3

import os
import sys
import logging

logging.basicConfig(level=logging.INFO)

s = "E2bywHLZ7M0bCGoh587KW7lX7Zc"
junk_low = "taco"
junk_up = "TACO"

def encode_file(source, destination):
    logging.info('Encoding {} into {}...'.format(source, destination))
    dest = open(destination, 'wb')
    cnt = 0
    with open(source, 'rb') as f:
        byte = f.read(1)
        val = ord(byte) ^ ord(s[cnt])
        while byte:
            for bit in range(8):
                if (val & (1 << bit) != 0):
                    dest.write(bytes(junk_low[bit % 4], 'ascii'))
                else:
                    dest.write(bytes(junk_up[bit % 4], 'ascii'))
            byte = f.read(1)
            cnt = (cnt + 1) % len(s)
            if byte:
                val = ord(byte) ^ ord(s[cnt])

if __name__ == '__main__':
    if len(sys.argv) == 3 and os.path.isfile(sys.argv[1]):
        encode_file(sys.argv[1], sys.argv[2])
