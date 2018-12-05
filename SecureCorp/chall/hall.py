#!/usr/bin/python

import random
import base64
from Crypto.Cipher import AES
from Crypto import Random
import json


# TOKEN MGMT
KEY_SIZE = 16
BLOCK_SIZE = AES.block_size


class DecryptionException(Exception):
    pass


def pad(m, bs=BLOCK_SIZE):
    pl = bs-(len(m)%bs)
    pl = bs if pl==0 else pl

    return m + chr(pl)*pl


def unpad(m, bs=BLOCK_SIZE):

    n = ord(m[-1])
    if n>bs:
        raise Exception

    pad = m[-n:]
    if len(set(pad))!=1:
        raise Exception

    return m[:-n]


# UNIT TEST
s = 'iansus'
assert(unpad(pad(s))==s)


def gen_token():
    guid = Random.new().read(KEY_SIZE).encode('hex')
    token = {'guid': guid, 'level': 'GUEST'}

    key = Random.new().read(KEY_SIZE)
    iv = Random.new().read(BLOCK_SIZE)
    token = json.dumps(token)
    token = pad(token)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    token = iv + cipher.encrypt(token)
    token = base64.b64encode(token)

    return token, key


def decrypt_token(token, key):

    try:
        token = base64.b64decode(token)
    except TypeError:
        raise DecryptionException('Malformed base64')

    if len(token)<BLOCK_SIZE:
        raise DecryptionException('Ciphertext is too short, cannot grab the IV')

    iv = token[:BLOCK_SIZE]
    token = token[BLOCK_SIZE:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    try:
        token = cipher.decrypt(token)
    except Exception, e:
        raise DecryptionException('Error on token AES decryption: %s' % (str(e)))

    try:
        token = unpad(token)
    except Exception, e:
        raise DecryptionException('Invalid padding in "%s"' % (token.encode('hex')))

    try:
        token = json.loads(token)
    except Exception, e:
        raise DecryptionException('Malformed JSON in "%s"' % (token.encode('hex')))

    return token


# These functions return if you need to send the flag and another optional message
def room_admin(token, key):

    try:
        token = decrypt_token(token, key)
        assert(token['level'] in ['ADMIN'])
        return True, 'ACCESS GRANTED %s !' % token['guid']

    except:
        return False, 'YOU DO NOT HAVE ACCESS'


def room_guest(token, key):
    try:
        token = decrypt_token(token, key)
        assert(token['level'] in ['ADMIN', 'GUEST'])
        return False, 'ACCESS GRANTED %s !' % token['guid']

    except:
        return False, 'YOU DO NOT HAVE ACCESS'


def room_debug(token, key):
    try:
        token = decrypt_token(token, key)
        assert(token['level'] in ['ADMIN', 'GUEST'])
        return False, 'ACCESS GRANTED %s !' % token['guid']

    except Exception, e:
        return False, str(e)



def gen_rooms():
    rooms = {'ADMIN': room_admin, 'GUEST': room_guest, 'DEBUG': room_debug}
    id_rooms = {}
    rooms_id = {}
    alphabet = range(100)

    for room in rooms:
        c = random.choice(alphabet)
        alphabet.remove(c)
        c = base64.b64encode(str(c))
        id_rooms[c] = (room, rooms[room])
        rooms_id[room] = c

    return id_rooms, rooms_id


### MAIN ###
if __name__=='__main__':
    token, key = gen_token()
    token = decrypt_token(token, key)
    print token
