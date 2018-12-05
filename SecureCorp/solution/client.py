#!/usr/bin/env python2

from pwn import *
import argparse
import base64
import sys

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('host', metavar='host', type=str)

    args = parser.parse_args()

    DELIM = '\n> '

    io = remote(args.host, 4445)
    data = io.recvuntil(DELIM)
    print data

    data = data.splitlines()
    BASE = -11
    codes = {
        data[BASE][2]: '0,0',
        data[BASE][6]: '0,1',
        data[BASE][10]: '0,2',
        data[BASE+2][2]: '1,0',
        data[BASE+2][6]: '1,1',
        data[BASE+2][10]: '1,2',
        data[BASE+4][2]: '2,0',
        data[BASE+4][6]: '2,1',
        data[BASE+4][10]: '2,2',
        data[BASE+6][6]: '3,1',
        ' ': '3,0',
    }

    code = [' ', ' ', ' ', ' ', ' ']
    found = False
    for i in range(len(code)):
        timemax = (0, None)

        for j in range(10):
            code[i] = str(j)
            coords = '|'.join([codes[e] for e in code])

            means = []
            for k in range(1):
                io.send('%s\n' % coords)
                data = io.recvuntil(DELIM)
                if 'OH GOOD' in data:
                    found = True
                    break

                t = float(data.splitlines()[0].split()[-3])
                print j, t
                means.append(t)

            if found:
                break

            t = sum(means)/len(means)
            if t > timemax[0]:
                timemax = (t, str(j))

        if not found:
            code[i] = timemax[1]

        print code

    print data
    token = data.splitlines()[3].split()[1]

    ROOMS = {}
    for i in range(100):
        code = base64.b64encode(str(i))
        io.send('%s|%s\n' % (code, token))
        data = io.recvuntil(DELIM)
        if not 'WELCOME TO ROOM' in data:
            continue

        data = data.splitlines()
        ROOMS[data[0].split('"')[1]] = code

    print 'Rooms are: %s' % str(ROOMS)


    def str2blk(s, bs=16):
        return [map(ord, list(s[i:i+bs])) for i in range(0, len(s), bs)]

    def blk2str(b):
        return ''.join([''.join(map(chr, e)) for e in b])

    def xor(a, b):
        return [c^d for c, d in zip(a, b)]

    BS = 16
    token = base64.b64decode(token)
    IV_blocks = str2blk(token[:BS])
    token_full = base64.b64encode(token + 'a'*BS)
    io.send('%s|%s\n' % (ROOMS['DEBUG'], token_full))
    data = io.recvuntil(DELIM)

    wanted_full = data.splitlines()[1].split('"')[1].decode('hex')
    print wanted_full
    wanted = wanted_full[:-BS]
    wanted = wanted.replace('GUEST', 'ADMIN')
    wanted_blocks = str2blk(wanted)

    token_blocks = str2blk(token)
    token_blocks[-1][-1] ^= 0x7f
    token = base64.b64encode(blk2str(token_blocks))
    io.send('%s|%s\n' % (ROOMS['DEBUG'], token))
    data = io.recvuntil(DELIM)

    blk = len(wanted_blocks)-1
    while blk>=0:
        clear_token = data.splitlines()[1].split('"')[1].decode('hex')
        clear_token_blocks = str2blk(clear_token)

        wanted_xor = xor(wanted_blocks[blk], clear_token_blocks[blk])
        token_blocks[blk] = xor(wanted_xor, token_blocks[blk])
        token = base64.b64encode(blk2str(token_blocks))
        io.send('%s|%s\n' % (ROOMS['DEBUG'], token))
        data = io.recvuntil(DELIM)
        blk -= 1

    io.send('%s|%s\n' % (ROOMS['ADMIN'], token))
    print io.recvall()

if __name__ == "__main__":
    main()
