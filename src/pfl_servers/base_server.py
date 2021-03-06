import logging
import socketserver
import sys
import threading
import os
import pickle
import logging

from pfl_types.datagram import Msg, RequestType

logging.basicConfig(level=logging.DEBUG)


class PFLHandler(socketserver.BaseRequestHandler):

    def handle_default(self, msg):
        '''
        Does default handling, returns true if
        msg was handled
        '''
        logging.debug('{} received {} from {}'.format(
            self.server.server_address, msg.req_type, self.client_address))
        if msg.req_type == RequestType.RESTART:
            # Kill ourselves and let the watchdog restart us
            logging.error('{} going down for restart'.format(
                self.SOCKET_PATH))
            self.server._BaseServer__shutdown_request = True
            return True
        elif msg.req_type == RequestType.PING:
            self.request.sendall(
                pickle.dumps(Msg(RequestType.PING_RESP, None)), )
            return True
        elif msg.req_type == RequestType.COMMAND:
            print('Executing command: {}'.format(msg.data))
            return False


class PFLServer(socketserver.UnixStreamServer):
    def handle_error(self, request, client_address):
        super(request, client_address)
        logging.error('Request {}\n could not be handled,'
                      ' terminating server...'.format(
                          request))
        sys.exit(5)


def start_server():
    logging.info('Initializing CDH server...')
    if os.path.exists(SOCKET_PATH):
        logging.warn('Detected stale socket, removing to start server...')
        os.remove(SOCKET_PATH)

    server = socketserver.UnixStreamServer(SOCKET_PATH, CDHHandler)
    try:
        server.serve_forever()
    finally:
        # Make sure to remove socket if handler crashes
        os.remove(SOCKET_PATH)


if __name__ == '__main__':
    start_server()
