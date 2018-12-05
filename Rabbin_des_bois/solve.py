#!/usr/bin/python

from pwn import process, remote, context
import argparse
import binascii
import logging
import sys

logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('host', metavar='host', type=str)

    args = parser.parse_args()

    def iterative_egcd(a, b):
        x,y, u,v = 0,1, 1,0
        while a != 0:
            q,r = b//a,b%a
            m,n = x-u*q,y-v*q
            b,a, x,y, u,v = a,r, u,v, m,n
        return b, x, y


    context.log_level = 'error'

    def init(args):
        p = remote(args.host, 8888, level='error')
        return p

    p = init(args)

    logger.debug(p.recvuntil("[.] For example 2:p "))

    p.sendline("3")
    p.sendline("")
    target_length = int(p.recvall().split("c = ")[1])

    p = init(args)
    logger.debug(p.recvuntil("[.] For example 2:p "))

    a1 = target_length*10
    b1 = target_length*11

    p.sendline("1")
    p.sendline(str(a1))
    p.sendline("")
    p.recvuntil("Result :\n")
    a2 = int(p.recvuntil("\n").split("m = ")[1].split("\n")[0])

    p.sendline("1")
    p.sendline(str(b1))
    p.sendline("")
    p.recvuntil("Result :\n")
    b2 = int(p.recvuntil("\n").split("m = ")[1].split("\n")[0])

    N = abs(iterative_egcd(a2-pow(a1,2),b2-pow(b1,2))[0])
    # print(N)

    p.sendline("2")
    p.sendline(str(a2))
    p.sendline("5:s")
    p.recvuntil("Result :\n")
    final = p.recvuntil("\n").split("m = ")[1].split("\n")[0]

    # print(final)

    f1 = iterative_egcd(N,int(final)+a1)[0]
    f2 = N//f1

    if len(str(f1)) <= len(str(N))//5 or len(str(f1)) >= 4*len(str(N))//5:
        f1 = iterative_egcd(N,int(final)-a1)[0]
        f2 = N//f1

    # print(f1)
    # print(f2)
    # print(N==f1*f2)

    tmp = p.recvall()
    c = int(tmp.split("c = ")[1].split("\n")[0])

    def decrypt(p, q, c):
        g, x, y = iterative_egcd(p,q)

        n = p*q

        r = (pow(c,((p+1)//4),p))
        s = (pow(c,((q+1)//4),q))

        r1 = ((x*p*s)+(y*q*r))%n
        r2 = ((x*p*s)-(y*q*r))%n
        r3 = n-r1
        r4 = n-r2

        return r1, r2, r3, r4

    def n_to_string(n):
        r = hex(n).replace("0x","").replace("L","")
        if len(r) % 2:
            return binascii.unhexlify("0"+r)
        else:
            return binascii.unhexlify(r)

    decrypted = decrypt(f1, f2, c)

    # print(decrypted)
    for a in decrypted:
        if n_to_string(a).find('sigsegv') != -1:
            print n_to_string(a)

if __name__ == "__main__":
    main()
