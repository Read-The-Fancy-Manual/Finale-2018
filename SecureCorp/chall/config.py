#!/usr/bin/python

import logging

# CONFIG PARAMETERS
LISTEN_ADDRESS = '0.0.0.0'
LISTEN_PORT = 4445

MAX_CLIENTS = 50
SOCKET_TIMEOUT = 30

# LOGGING
logging.basicConfig(format = '\r[%(asctime)s] %(name)-15s %(levelname)-9s %(message)s')
logging.getLogger('').setLevel(logging.INFO)
