import socket
import select
from PIL import Image
import copy
from pprint import pprint

LISTEN_PORT = 10000
RECV_BUFFER = 1024
FLAG = open('/home/chall/flag.txt', 'r').read()
#STARTING_COORDINATES = {'x': 90, 'y': 265}
STARTING_COORDINATES = {'x': 50, 'y': 180}

WELCOME_MESSAGE = """
 ██▓    ▄▄▄       ▄▄▄▄ ▓██   ██▓▓█████▄  █    ██  ██▓     ██▓ ███▄    █ ▄▄▄█████▓ ██░ ██ ▓█████ 
▓██▒   ▒████▄    ▓█████▄▒██  ██▒▒██▀ ██▌ ██  ▓██▒▓██▒    ▓██▒ ██ ▀█   █ ▓  ██▒ ▓▒▓██░ ██▒▓█   ▀ 
▒██░   ▒██  ▀█▄  ▒██▒ ▄██▒██ ██░░██   █▌▓██  ▒██░▒██░    ▒██▒▓██  ▀█ ██▒▒ ▓██░ ▒░▒██▀▀██░▒███   
▒██░   ░██▄▄▄▄██ ▒██░█▀  ░ ▐██▓░░▓█▄   ▌▓▓█  ░██░▒██░    ░██░▓██▒  ▐▌██▒░ ▓██▓ ░ ░▓█ ░██ ▒▓█  ▄ 
░██████▒▓█   ▓██▒░▓█  ▀█▓░ ██▒▓░░▒████▓ ▒▒█████▓ ░██████▒░██░▒██░   ▓██░  ▒██▒ ░ ░▓█▒░██▓░▒████▒
░ ▒░▓  ░▒▒   ▓▒█░░▒▓███▀▒ ██▒▒▒  ▒▒▓  ▒ ░▒▓▒ ▒ ▒ ░ ▒░▓  ░░▓  ░ ▒░   ▒ ▒   ▒ ░░    ▒ ░░▒░▒░░ ▒░ ░
░ ░ ▒  ░ ▒   ▒▒ ░▒░▒   ░▓██ ░▒░  ░ ▒  ▒ ░░▒░ ░ ░ ░ ░ ▒  ░ ▒ ░░ ░░   ░ ▒░    ░     ▒ ░▒░ ░ ░ ░  ░
  ░ ░    ░   ▒    ░    ░▒ ▒ ░░   ░ ░  ░  ░░░ ░ ░   ░ ░    ▒ ░   ░   ░ ░   ░       ░  ░░ ░   ░   
    ░  ░     ░  ░ ░     ░ ░        ░       ░         ░  ░ ░           ░           ░  ░  ░   ░  ░
                       ░░ ░      ░                                                              

                        Welcome in the Labydulinthe!             

Mischievously designed by Bidulette, this maze will probably be your last home. MOUAHAHAH

Commands:
 - N / NORTH
 - S / SOUTH
 - W / WEST
 - E / EST

Good luck getting out of this maze!
"""

class LabydulintheSocketServer:
    CONNECTION_LIST = {}    # list of socket clients
    POSITIONS = {}

    def __init__(self, sock=None):
        # image = Image.open('./map.png')
        image = Image.open('/home/chall/map.jpg')
        self.map_size = image.size
        self.map = image.load()
        self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 0)
        self.serversocket.bind(("0.0.0.0", LISTEN_PORT))

    def listen(self):
        self.serversocket.listen(10)
        print('[i] Labydulinthe socket server started.')
        while True:
            ALL_CONS = {}
            for k,v in self.CONNECTION_LIST.items():
                ALL_CONS[k] = v.fileno()
            for k,v in ALL_CONS.items():
                if v == -1:
                    del self.CONNECTION_LIST[k]
            try :
                read_sockets, write_sockets, error_sockets = select.select([self.serversocket] + list(self.CONNECTION_LIST.values()), [], [])
            except ValueError as e:
                print(e)
                print(self.serversocket)
                print(self.CONNECTION_LIST)
                sys.exit()
            for sock in read_sockets:
                # New connection
                if sock == self.serversocket:
                    # Handle the case in which there is a new connection recieved through serversocket
                    sockfd, addr = self.serversocket.accept()
                    self.CONNECTION_LIST[sockfd.fileno()] = sockfd
                    print("[+] Client (%s) connected - fd: %s" % (addr, sockfd.fileno()))
                    self.POSITIONS[sockfd.fileno()] = copy.deepcopy(STARTING_COORDINATES)
                    sockfd.send(bytes(WELCOME_MESSAGE, encoding='utf-8'))
                    sockfd.send(bytes('Size of the maze : width : %s - height : %s\n' % (self.map_size[0], self.map_size[1]), encoding='utf-8'))
                    sockfd.send(bytes('Your actual position is : x : %s - y : %s\n' % (self.POSITIONS[sockfd.fileno()]['x'], self.POSITIONS[sockfd.fileno()]['y']), encoding='utf-8'))
                    sockfd.send(bytes('> ', encoding='utf-8'))
                # Some incoming message from a client
                else:
                    # Data recieved from client, process it
                    try:
                        # In Windows, sometimes when a TCP program closes abruptly,
                        # a "Connection reset by peer" exception will be thrown
                        data = sock.recv(RECV_BUFFER)
                        # echo back the client message
                        if data:
                            move = data.decode('utf-8').replace('\n', '')
                            position = copy.deepcopy(self.POSITIONS[sock.fileno()])
                            old_position = copy.deepcopy(position)
                            if move.lower() in ['n', 'north']:
                                position['y'] += 1
                            elif move.lower() in ['s', 'south']:
                                position['y'] -= 1
                            elif move.lower() in ['w', 'west']:
                                position['x'] -= 1
                            elif move.lower() in ['e', 'est']:
                                position['x'] += 1
                            else:
                                sock.send(bytes('Commande inconnue.\n> ', encoding='utf-8'))
                                continue
                            map_color = self.map[position['x'], self.map_size[1] - position['y']]
                            self.POSITIONS[sock.fileno()] = position

                            if map_color[1] > 200 or (map_color[0] > 100 and map_color[1] > 100 and map_color[2] > 100) : # White / green zone
                                sock.send(bytes('OK - your new position is (%s - %s)\n' % (self.POSITIONS[sock.fileno()]['x'], self.POSITIONS[sock.fileno()]['y']), encoding='utf-8'))
                            elif map_color[0] > 200 and map_color[1] < 100 and map_color[2] < 100: # finish, nice !
                                print('    [+] Client %s won the game' % sock.fileno())
                                del self.POSITIONS[sock.fileno()]
                                del self.CONNECTION_LIST[sock.fileno()]
                                sock.send(bytes("You see some light at the end of the corridor...", encoding='utf-8'))
                                sock.send(bytes("Following your path you can finally breathe fresh air : You are out!", encoding='utf-8'))
                                sock.send(bytes("Congratulations! Outside you can read a strange inscription on a wooden sign: %s" % FLAG, encoding='utf-8'))
                                sock.shutdown(socket.SHUT_RDWR)
                                sock.close()
                                break
                            else: # Wall 
                                self.POSITIONS[sock.fileno()] = old_position
                                sock.send(bytes("STOMP ! You hit a wall, you stay at your last position (%s - %s).\n" %
                                    (self.POSITIONS[sock.fileno()]['x'], self.POSITIONS[sock.fileno()]['y']), encoding='utf-8'))
                        else:
                            addr = sock.getsockname()[0]
                            print('[-] Client (%s, %s) connection lost' % (sock.fileno(), addr))
                            try:
                                sock.shutdown(socket.SHUT_RDWR)
                                sock.close()
                            except OSError as e:
                                pass
                            if sock.fileno() in self.POSITIONS:
                                del self.POSITIONS[sock.fileno()]
                            if sock.fileno() in self.CONNECTION_LIST:
                                del self.CONNECTION_LIST[sock.fileno()]

                    # client disconnected, so remove from socket list
                    except (ConnectionResetError, Exception) as e:
                        print(e)
                        print('[-] Client (%s, %s) connection lost' % (sock.fileno(), addr))
                        try:
                            sock.shutdown(socket.SHUT_RDWR)
                            sock.close()
                        except OSError as e:
                            pass
                        if sock.fileno() in self.POSITIONS:
                            del self.POSITIONS[sock.fileno()]
                        if sock.fileno() in self.CONNECTION_LIST:
                            del self.CONNECTION_LIST[sock.fileno()]
                        continue

def main():
    lss = LabydulintheSocketServer()
    lss.listen()

if __name__ == '__main__':
    main()
