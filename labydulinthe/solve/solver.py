#!/usr/bin/env python
# coding: utf-8

import sys
import socket
from PIL import Image, ImageDraw
import argparse
import time
import random
import shutil

class Solver():

    moves = 0

    def __init__(self, host, port):
        self.im = Image.new('RGB', (1500, 1000), (200, 200, 200))
        self.draw = ImageDraw.Draw(self.im)
        self.matrix = [[0 for i in range(1500)] for j in range(1500)]
        self.matrix[90][265] = 9000
        self.host = host
        self.port = port

    def connect(self):
        self.x = 90
        self.y = 265
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((self.host, self.port))
        self.recv()
        print('[*] Connected to %s:%s' % (self.host, self.port))

    def send(self, msg):
        self.moves += 1
        try:
            self.s.send(bytes(msg, encoding='utf-8'))
        except socket.error as e:
            self.connect()
        # print('> %s' % msg)

    def recv(self):
        return str(self.s.recv(15000), encoding='utf-8')

    def run(self):
        self.connect()
        last_dir = "N"
        while 1:
            directions = {
                'N': self.matrix[self.x][self.y + 1],
                'S': self.matrix[self.x][self.y - 1],
                'W': self.matrix[self.x - 1][self.y],
                'E': self.matrix[self.x + 1][self.y],
            }
            d = min(list(directions.values()))
            candidates_dir = [x for x in directions.keys() if directions[x] == d]
            # print('RANDOM from : %s' % candidates_dir)
            used_dir = random.choice(candidates_dir)
            last_dir = used_dir

            self.send(used_dir)
            r = self.recv().replace('\n', '').strip().lower()

            if r.find('stomp') != -1: # if we encounter a wall ponderate that a lot so we don't go in it again
                if used_dir == 'N':
                    self.matrix[self.x][self.y + 1] += 999999999999
                if used_dir == 'S':
                    self.matrix[self.x][self.y - 1] += 999999999999
                if used_dir == 'W':
                    self.matrix[self.x - 1][self.y] += 999999999999
                if used_dir == 'E':
                    self.matrix[self.x + 1][self.y] += 999999999999
                # self.draw.point((self.x, 763-self.y), fill=(255, 0, 0))
                # self.im.save('./out_.png')
                # shutil.copyfile('./out_.png', './out.png')
            elif r.find('new position') != -1:
                self.draw.point((self.x, 763-self.y), fill=(100, 100, 100))
                if used_dir == 'N':
                    self.y += 1
                elif used_dir == 'S':
                    self.y -= 1
                elif used_dir == 'W':
                    self.x -= 1
                elif used_dir == 'E':
                    self.x += 1
                self.matrix[self.x][self.y] += 1 # ponderate the pixel we are on by one point so we don't want to come here next time
            if r.find('sigsegv') != -1:
                print(r)
                self.s.close()
                return
            # print(r, self.x, self.y)

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('host', metavar='host', type=str)
    #parser.add_argument('port', metavar='port', type=int)

    args = parser.parse_args()

    t_start = time.time()

    s = Solver(args.host, 10000)
    s.run()

    duration = time.time() - t_start
    readable_duration = time.strftime('%Hh%Mm%Ss', time.gmtime(duration))
    print('solved in %s moves - %s' % (s.moves, readable_duration))

if __name__ == '__main__':
    main()
