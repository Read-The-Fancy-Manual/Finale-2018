#!/usr/bin/python

import hashlib
import json
import logging
import random
import socket
import threading
import time

import entrance
import hall

ENTRANCE_STRING='''
>>> WELCOME TO SECURE CORP
>>> THIS IS OUR BUILDING

        ________________
       /                \\
      /   SECURE__CORP   \\
     /____________________\\
        ||            ||
        ||     __     ||
        ||    | .|    ||
     ___||____|__|____||___
    |______________________|

A challenge provided by iansus (Wavestone)

>>> YOU'LL NEVER GET PAST THE FRONT DOOR
>>> OUR SECURE SYSTEM CHANGES THE CODE EVERY TIME A NEW PERSON PRESENTS ITSELF

'''

HALL_STRING='''>>> THIS IS WHAT YOU SEE:

+--------------------------------------------------------------+
|                                                              |
|                                                              |
|                                                              |
|   +-----------+        +-----------+      +-----------+      |
|   |   ADMIN   |        |   GUEST   |      |   /x#@-   |      |
|   |   %5s   |        |   %5s   |      |   [:$*;   |      |
|   |           |        |           |      |           |      |
|   |         o |        |         o |      |         o |      |
|   |           |        |           |      |           |      |
|   |           |        |           |      |           |      |
|   |           |        |           |      |           |      |
+--------------------------------------------------------------+


'''


f = open('__flag', 'rb')
FLAG = f.read()
f.close()

class SocketHandler(threading.Thread):

    def __init__(self, client, addr):

        # SUPER
        threading.Thread.__init__(self)

        # ATTRIBUTES
        self.__threadname = hashlib.new('sha1', str(time.time())).hexdigest()[:6]
        self.__client = client
        self.__addr = addr
        self.__logger = logging.getLogger('client.%s' % self.__threadname)
        self.alive = True

        self.__client.settimeout(30)
        self.__logger.info('Client (%s, %d) joined' % self.__addr)


    def send(self, data):
        self.__client.send(data)
        self.__logger.debug('Sent "%s" to client' % data.replace('\n', '\\n'))


    def recv(self, l=1024):
        data = self.__client.recv(l)
        self.__logger.debug('Recvd "%s" from client' % data.replace('\n', '\\n'))
        return data


    def run(self):

        # GAME ON OLD FRIEND!
        try:
            ACCESS_CODE = entrance.gen_access_code()
            KEYBOARD = entrance.gen_random_keyboard()
            SLEEP_TIME=0.0876

            self.send(ENTRANCE_STRING)
            self.send('>>> THIS IS THE KEYBOARD\n\n')
            self.send(entrance.keyboard_to_text(KEYBOARD))

            while True:
                self.send('\n>>> PLZ PROVIDE YOUR 5-DIGIT CODE "x0,y0|x1,y1|x2,y2|x3,y3|x4,y4", (0,0) BEING TOP-LEFT CORNER\n> ')

                coords = self.recv(1024)
                try:
                    keys = entrance.textpos_to_keys(KEYBOARD, coords.strip())

                except Exception, e:
                    self.send('XXX INVALID COORDINATES %s!\n' % coords)
                    continue

                t = time.time()
                if entrance.secure_verif(ACCESS_CODE, keys, SLEEP_TIME):
                    self.send('>>> OH GOOD, IT\'S YOU :-)\n')
                    break

                else:
                    t2 = time.time()
                    self.send('>>> OUR SYSTEM DETERMINED YOU\'RE A FRAUD IN ONLY %.4f SECONDS !!\n' % (t2-t))


            # Entering hall
            ID_ROOMS, ROOMS_ID = hall.gen_rooms()
            encrypted_token, KEY = hall.gen_token()

            self.send('>>> ENTERING HALL, YOU SEE WALLS MOVING AND ROOMS CHANGING PLACE!\n')
            self.send('>>> SOMEONE TAPS ON YOUR BACK, YOU TURN AROUND AND HE GIVES YOU THIS TOKEN:\n')
            self.send('>>> %s\n' % encrypted_token)
            self.send('>>> WHEN YOU TURN BACK, THE HALL IS NOW STABILIZED:\n')
            self.send(HALL_STRING % (ROOMS_ID['ADMIN'], ROOMS_ID['GUEST']))

            while True:
                self.send('>>> GIVE ME A ROOM CODE AND YOUR TOKEN TO ENTER IT!\n')
                self.send('>>> FORMAT IS ROOM_CODE|TOKEN\n')
                self.send('> ')

                data = self.recv(1024).strip()
                if not '|' in data:
                    self.send('>>> ERROR: MALFORMED ENTRY\n')
                    continue

                roomid, token = data.split('|', 1)
                if not roomid in ID_ROOMS.keys():
                    self.send('>>> YOU HIT THE WALL, THAT ROOM DOES NOT EXIST...\n')
                    continue

                roomname, func = ID_ROOMS[roomid]
                self.send('>>> WELCOME TO ROOM "%s"\n' % roomname)
                print_flag, message = func(token, KEY)
                self.send('>>> %s\n' % message)

                if print_flag:
                    self.send('>>> %s\n' % FLAG)
                    break


        except socket.error:
            self.__logger.info('Client disconnected')

        self.__exit()
        return


    def __exit(self):
        self.__client.close()
        self.__logger.info('Exiting')
        self.alive = False



# UNIT TEST
if __name__=='__main__':
    pass
