#!/usr/bin/env python3

import camellia
import argparse
import requests
import hashlib
import base64
import string
import pydle
import time
import sys
import re

class Chall(pydle.Client):
    def on_connect(self):
        super().on_connect()
        # start chall
        print('-> [Apox] !part1')
        self.message('Apox', '!part1')
        self.flag = ''
    # Decipher this, you have 3 seconds to answer. cipher: camellia256, key: nKEDtu0mrWc2G+6uEljgbF0gU/BPfDKp+F7DFzzb8Ds=, iv: I3nT1RfznZtRuPymoOdtkg==, encrypted: LySP5Iy0pf+npss0c3FUyA==
    def on_private_message(self, by, message):
        print('<- [%s] %s' % (by, message))
        # part1
        if message.startswith('Crack this md5 hash'):
            m = re.findall('Crack this md5 hash: ([^,]+)', message)
            hash = m[0].replace(':', '')
            print('[*] got hash %s' % hash)
            data = {'md5':hash}
            r = requests.post('http://md5.my-addr.com/md5_decrypt-md5_cracker_online/md5_decoder_tool.php', data=data)
            m = re.findall('Hashed string<\/span>:([^<]+)', r.text)
            if len(m) == 0:
                print('[-] Failed to find reverse hash')
            else:
                reverse = m[0].strip().rstrip()
                print('-> [Apox] !part1 -ans %s' % reverse)
                self.message(by, '!part1 -ans %s' % reverse)
        elif message.startswith('Part 1 of the Flag: '):
            m = re.findall('Part 1 of the Flag: (.*)', message)
            self.flag += m[0]
            print('[*] flag: %s' % self.flag)
            print('-> [Apox] !part2')
            self.message(by, '!part2')
        elif message.startswith('Decipher this,'):
            m = re.findall('Decipher this, you have 3 seconds to answer. cipher: camellia256, key: ([^,]+), iv: ([^,]+), encrypted: (.*)', message)
            self.key = base64.b64decode(m[0][0].strip().rstrip())
            self.iv = base64.b64decode(m[0][1].strip().rstrip())
            self.encrypted = base64.b64decode(m[0][2].strip().rstrip())
            c = camellia.CamelliaCipher(key=bytes(self.key), IV=bytes(self.iv), mode=camellia.MODE_CBC)
            plain = c.decrypt(self.encrypted)
            res = ''.join([chr(c) for c in plain if chr(c) in string.digits + string.ascii_letters])
            print('-> [Apox] !part2 -ans %s' % res.strip().rstrip())
            self.message(by, '!part2 -ans %s' % res.strip().rstrip())
        elif message.startswith('Part 2 of the Flag: '):
            m = re.findall('Part 2 of the Flag: (.*)', message)
            self.flag += m[0].strip().rstrip()
            print('[*] flag: %s' % self.flag)
            print('-> [Apox] !part3')
            self.message(by, '!part3')
        elif message.startswith('Give me the number of times this password: '):
            m = re.findall('Give me the number of times this password: ([^,]+)', message)
            password = m[0].strip().rstrip()
            hash = hashlib.sha1(bytes(password, 'ascii')).hexdigest().upper()
            headers = {'User-Agent':'Challenger'}
            r = requests.get('https://api.pwnedpasswords.com/range/' + hash[:5], headers=headers)
            dic = dict()
            for line in r.text.split():
                data = line.split(':')
                dic[data[0]] = data[1]
            res = dic.get(hash[5:])
            print('-> [Apox] !part3 -ans %s' % res)
            self.message(by, '!part3 -ans %s' % res)
        elif message.startswith('Part 3 of the Flag: '):
            m = re.findall('Part 3 of the Flag: (.*)', message)
            self.flag += m[0]
            print('[+] got flag: %s' % self.flag)
            self.disconnect()

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('host', metavar='host', type=str)

    args = parser.parse_args()

    client = Chall('laxa')
    client.connect(args.host, port=6697, tls=True)

    try:
        client.handle_forever()
    except KeyboardInterrupt:
        client.disconnect()

if __name__ == "__main__":
    main()
