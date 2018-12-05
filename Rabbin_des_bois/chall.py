#!/usr/bin/python

from Crypto.Util import number
from flag import flag
import binascii
import random
import sys
import re
import os


def generate(bits=512):
    p = number.getPrime(bits)
    while p%4 != 3:
        p = number.getPrime(bits)
    q = number.getPrime(bits)
    while q%4 != 3:
        q = number.getPrime(bits)

    N = p*q
    return (N,p,q)


def iterative_egcd(a, b):
    x,y, u,v = 0,1, 1,0
    while a != 0:
        q,r = b//a,b%a
        m,n = x-u*q,y-v*q
        b,a, x,y, u,v = a,r, u,v, m,n
    return b, x, y


encrypt_str = """
c = pow(m,2) % n
"""

decrypt_str = """
g, x, y = iterative_egcd(p,q)
n = p*q
r = (pow(c,((p+1)//4),p))
s = (pow(c,((q+1)//4),q))
r1 = ((x*p*s)+(y*q*r))%n
r2 = ((x*p*s)-(y*q*r))%n
r3 = n-r1
r4 = n-r2
"""

def modify(msg,line,var):
    split = msg.split('\n')
    if line<len(split):
        tmp = split[:line]
        tmp.append(var+' = random.randint(3,2**512)')
        tmp.extend(split[line:])
        return '\n'.join(tmp)
    else:
        return msg

def encrypt_with_modif(m,modif):
    global key
    matched = re.search('([0-9])*:([a-z0-9]{1,2})',modif)
    if matched is not None:
        to_exec = modify(encrypt_str,int(matched.group(1)),matched.group(2))
    else:
        to_exec = encrypt_str

    n = key[0]
    exec(to_exec)

    print("[+] Result :")
    print("m = "+str(c))
    sys.stdout.flush()

def decrypt_with_modif(c,modif):
    global key
    matched = re.search('([0-9])*:([a-z0-9]{1,2})',modif)
    if matched is not None:
        to_exec = modify(decrypt_str,int(matched.group(1)),matched.group(2))
    else:
        to_exec = decrypt_str

    print(to_exec)
    p = key[1]
    q = key[2]
    exec(to_exec)

    print("[+] Result :")
    #print("m = "+str((r1,r2,r3,r4)))
    print("m = "+str(r4))
    sys.stdout.flush()

depends = {'1':'ciphered','2':'deciphered'}
func = {'1':encrypt_with_modif,'2':decrypt_with_modif}

if __name__ == "__main__":
    if len(sys.argv) > 1:
        key = (164549871995089586174717684958603023332539451801957097331382951593502137959692718870158752986334673911644281073574812766375369686380776510880966496248751786504852645281295636954562620171698816272880977010296029201824768871658633623534172265073665007784033664509718004593590102100873203038780919307372944438553L, 12555440445693047298758148930986854343941498265201260018507328036070259832776431177389037724363094804768714786799550436307849981430298518121717452654999607L, 13105862172404785262651607677183511647553042404759414333220766197127164966181459227416221362848690806095646687932810981710722255089347106330177500943512879L)
        print(key)
        sys.stdout.flush()
    else:
        key = generate()

    print("[+] Key generated")

    print("[.] You have the choice doing :")
    print("   - 1 : Encryption")
    print("   - 2 : Decryption")
    print("   - 3 : Get flag and exit")
    print("[.] You can query the options 1 and 2 3 times (option 3 is automatic after that), and it will propose you to modify one line of encryption or decryption module every time")
    print("[.] Format concerning line modification is [line]:[variable]")
    print("[.] For example 2:p will add 'p = random.randint(3,2**512)' before 'n = p*q' in decryption process if you're in decryption module")
    sys.stdout.flush()

    leave = False
    for i in range(3):
        print("[?] Your choice :")
        sys.stdout.flush()
        raw = raw_input()
        if raw != '1' and raw != '2' and raw != '3':
            print("[-] Bad input")
            sys.stdout.flush()
            exit()
        elif raw == '3':
            leave = True
            break
        else:
            print("[?] Your number to be "+depends[raw]+" :")
            sys.stdout.flush()
            m = raw_input()
            matched = re.match('^([0-9]*)$',m)
            if matched is None:
                print("[-] Bad input, waiting for number")
                sys.stdout.flush()
                exit()
            print("[?] Your modification in code (could be empty) :")
            sys.stdout.flush()
            modif = raw_input()

            func[raw](int(matched.group(1)),modif)

    if not leave:
        print("[.] No more attempts")
    print("[.] Ciphered flag is : ")
    sys.stdout.flush()
    m = int(binascii.hexlify(flag),16)
    n = key[0]
    exec(encrypt_str)
    print("c = "+str(c))
    sys.stdout.flush()
