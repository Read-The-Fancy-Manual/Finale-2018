#!/usr/bin/python

import config
import program

import logging
import socket
import sys

logger = logging.getLogger('server')
logger.info('Server started')

# CREATE SOCKET
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(config.SOCKET_TIMEOUT)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
logger.debug('Socket created')

# BIND SOCKET
s.bind((config.LISTEN_ADDRESS, config.LISTEN_PORT))
s.listen(config.MAX_CLIENTS)
logger.debug('Socket configured')

activeClients = []
logger.info('Waiting for clients')
while True:
    
    for client in activeClients:
        if not client.alive:
            activeClients.remove(client)
    
    try:
        clientSock, clientAddr = s.accept()
        logger.debug('Client (%s, %d) connected - %d active clients' % (clientAddr[0], clientAddr[1], len(activeClients)))
        sh = program.SocketHandler(clientSock, clientAddr)
        activeClients.append(sh)
        sh.daemon = True
        sh.start()
        
    except socket.timeout:
        logger.debug('No client accepted within %d seconds - %d active clients' % (config.SOCKET_TIMEOUT, len(activeClients)))
