#!/usr/bin/python

import hashlib
import random
import time

CHARSET = range(0, 10)
SECRET_KEY = 'noonewillfindthis!'

# Hash function
def _digest(s, sleep_time):
    delta = sleep_time/5
    time.sleep(sleep_time + (random.random()-0.5)*delta)
    return str(s)


def secure_verif(code, access_code, sleep_time):
    if len(code)!=len(access_code):
        return False

    for a, b in zip(code, access_code):
        if _digest(a, sleep_time)!=_digest(b, sleep_time):
            return False
    return True


def keyboard_to_text(kbd):
    kbd = [(''.join(['| %s ' % e for e in kbd[i:i+3]]) + '|\n') for i in range(0, len(kbd), 3)]
    sep = '+---+---+---+\n'
    text = sep.join(kbd)
    text = sep + text + sep
    text = sep + '| >KEYBOARD |\n' + text

    return text


def _pos_to_key(kbd, pos):
    y, x = map(int, pos)
    assert x>=0 and x<3
    assert y>=0 and y<4

    k = kbd[3*y+x]

    return k

def textpos_to_keys(kbd, textpos):
    t = map(lambda x: x.split(',')[:2], textpos.split('|'))
    r = map(str, [_pos_to_key(kbd, e) for e in t])

    return r


def gen_access_code():
    ACCESS_CODE_LEN = 5
    ACCESS_CODE = [random.choice(CHARSET) for i in range(ACCESS_CODE_LEN)]

    return ACCESS_CODE


def gen_random_keyboard():
    KEYBOARD = [e for e in CHARSET]
    random.shuffle(KEYBOARD)
    KEYBOARD = map(str, KEYBOARD)
    KEYBOARD = KEYBOARD[:9] + [' '] + [KEYBOARD[9]] + [' ']

    return KEYBOARD
