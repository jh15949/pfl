import logging
import socketserver
import sys
import threading
import os
import pickle
import logging

from cpos_types.datagram import Msg, RequestType, ADCSCommand
from cpos_servers.fast_socket import FastSocket

SOCKET_PATH = '/tmp/adcs'
logging.basicConfig(level=logging.INFO)


class ADCSHandler(socketserver.BaseRequestHandler):
    def handle(self):
        msg = pickle.loads(self.request.recv(1024))
        logging.debug('{} received {} from {}'.format(SOCKET_PATH, msg.req_type, self.client_address))
        if msg.req_type == RequestType.RESTART:
            # Kill ourselves and let the watchdog restart us
            raise Exception('CDH going down for restart')
        elif msg.req_type == RequestType.PING:
            self.request.sendall(
                pickle.dumps(Msg(RequestType.PING_RESP, None)), 
            )
        elif msg.req_type == RequestType.COMMAND:
            print('Executing command: {}'.format(msg.data))
            if msg.data == ADCSCommand['IS_TUMBLING']:
                result = self.is_tumbling()
                self.request.sendall(
                    pickle.dumps(Msg(RequestType.DATA, result))
                )

    def is_tumbling(self):
        return False

def start_server():
    logging.info('Initializing ADCS server...')
    if os.path.exists(SOCKET_PATH):
        logging.warn('Detected stale socket, removing to start server...')
        os.remove(SOCKET_PATH)

    server = socketserver.UnixStreamServer(
        SOCKET_PATH,
        ADCSHandler
    )
    try:
        server.serve_forever()
    finally:
        # Make sure to remove socket if handler crashes
        os.remove(SOCKET_PATH)

if __name__ == '__main__':
    start_server()