from socket import *
from datetime import datetime
import sys
import argparse

from common.constants import *
from common.utils import *

from decorators import log

import logs.client_log_config
CLIENT_LOGGER = logging.getLogger('client')


class Client():

    def __init__(self, server_address = DEFAULT_IP_ADDRESS, server_port = DEFAULT_PORT, logger = CLIENT_LOGGER, client_mode = 'listen'):
        self.logger = logger
        
        parser = argparse.ArgumentParser()
        parser.add_argument('addr', default=DEFAULT_IP_ADDRESS, nargs='?')
        parser.add_argument('port', default=DEFAULT_PORT, type=int, nargs='?')
        parser.add_argument('-m', '--mode', default='listen', nargs='?')
        namespace = parser.parse_args(sys.argv[1:])
        self.server_address = namespace.addr
        self.server_port = namespace.port
        self.client_mode = namespace.mode
        
        if not 1023 < server_port < 65536:
            self.critical(f'Undefined port (must be in range from 1024 to 65535): {self.server_port}.')
            sys.exit(1) 

        if self.client_mode not in ('listen', 'send'):
            self.logger.critical(f'Undefined mode: {self.client_mode}.')
            sys.exit(1)



    @log
    def make_presense(self, account_name='Guest'):

        self.logger.debug(f'Created {PRESENCE}-message for {account_name}')

        return {
            ACTION: PRESENCE,
            TIME: datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            TYPE: STATUS,
            USER: {
                ACCOUNT_NAME: account_name,
                STATUS: HERE
            }
        }

    @log
    def create_message(self, sock, account_name='Guest'):
        message = input('Message: ')
        if message == 'exit()':
            sock.close()
            self.logger.info('Shutting down')
            print('Shutting down')
            sys.exit(0)
        message_dict = {
            ACTION: MESSAGE,
            TIME: datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            ACCOUNT_NAME: account_name,
            MESSAGE_TEXT: message
        }
        self.logger.debug(f'Created {MESSAGE}-message for {account_name}')
        return message_dict
    
    @log
    def message_from_server(self,message):
        if ACTION in message and message[ACTION] == MESSAGE and \
                SENDER in message and MESSAGE_TEXT in message:
            print(f'Message from: {message[SENDER]}:\n{message[MESSAGE_TEXT]}')
            self.logger.info(f'Message from: {message[SENDER]}:\n{message[MESSAGE_TEXT]}')
        else:
            self.logger.error(f'Bad message from server: {message}')
    
    @log
    def process_ans(self, response):

        self.logger.debug(f'Processing response from server: {response}')

        if RESPONSE in response:
            if response[RESPONSE] == 200:
                return f'Response code: {response[RESPONSE]}\nAlert: {response[ALERT]}'
            return f'Response code: {response[RESPONSE]}\nError: {response[ERROR]}'
        raise Exception

    def connect(self):    
        try:
            self.logger.info(
                f'Trying to connect to {self.server_address}:{self.server_port}.')
            socket_ = socket(AF_INET, SOCK_STREAM)
            socket_.connect((self.server_address, self.server_port))
            self.logger.info(
                f'Successfully connected to {self.server_address}:{self.server_port}.')
            request_to_server = self.make_presense()
            send_message(socket_, request_to_server)
        except ConnectionRefusedError:
            self.logger.error(
                f'Connection refused: {self.server_address}:{self.server_port}')
            sys.exit(1)
        except Exception as error:
            self.logger.error(f'Connection error: {error}:{self.server_port}')
            sys.exit(1)
            
        else: 
            if self.client_mode == 'send':
                print('SEND')
            else:
                print('LISTEN')
            while True:
                if self.client_mode == 'send':
                    try:
                        send_message(socket_, self.create_message(socket_))
                    except (ConnectionResetError, ConnectionError, ConnectionAbortedError):
                        self.logger.error(f'Connection lost: {self.server_address}.')
                        sys.exit(1)

                # Режим работы приём:
                if self.client_mode == 'listen':
                    try:
                        self.message_from_server(get_message(socket_))
                    except (ConnectionResetError, ConnectionError, ConnectionAbortedError):
                        self.logger.error(f'Connection lost: {self.server_address}.')
                        sys.exit(1)



if __name__ == '__main__':
    cl = Client()
    cl.connect()
