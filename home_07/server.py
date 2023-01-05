from socket import *
import sys

from common.constants import *
from common.utils import *

import logging
import logs.server_log_config

import select

from decorators import log

from datetime import datetime

SERVER_LOGGER = logging.getLogger('server')

class Server():
    
    def __init__(self, listen_port = DEFAULT_PORT, listen_address = '', logger = SERVER_LOGGER, max_connections = MAX_CONNECTIONS):
        self.logger = logger
        self.max_connections = max_connections
        try:
            if '-p' in sys.argv:
                self.listen_port = int(sys.argv[sys.argv.index('-p') + 1])
            else:
                self.logger.info( f'Port set to default {listen_port}')
                self.listen_port = listen_port
            if self.listen_port < 1024 or self.listen_port > 65535:
                raise Exception
        except IndexError:
            self.logger.error( f'Invalid port (-p) input (must be in range from 1024 to 65535) while starting')
            sys.exit(1)

        try:
            if '-a' in sys.argv:
                self.listen_address = sys.argv[sys.argv.index('-a') + 1]
            else:
                self.listen_address = listen_address
                self.logger.info( f'Adress set to default {listen_address}')
        except Exception:
            self.logger.error( f'Invalid adress (-a) input while starting')
            print('Enter the value of adress (-a)')
            sys.exit(1)
    
    @log
    def process_client_request(self, request, requests_list, client):
        
        self.logger.info('Processing client request')
        
        if ACTION in request and request[ACTION] == PRESENCE and TIME in request and USER in request:
            self.logger.info('Succsessfully processed')
            return {RESPONSE: 200,
                    ALERT: 'Connected'}
        
        elif ACTION in request and request[ACTION] == MESSAGE and TIME in request and MESSAGE_TEXT in request:
            requests_list.append((request[ACCOUNT_NAME], request[MESSAGE_TEXT]))
            self.logger.info('Succsessfully processed')
            return {RESPONSE: 200,
                    ALERT: 'Sended'}
            
        else:
            self.logger.info('Bad request processed')
            return {
                RESPONSE: 400,
                ERROR: 'Bad Request'
            }
    
    
    @log
    def start(self):
        try:
            self.logger.info( f'Trying to start server: {self.listen_address}:{self.listen_port}')
            socket_ = socket(AF_INET, SOCK_STREAM)
            socket_.bind((self.listen_address, self.listen_port))
            socket_.settimeout(0.3)
            
            clients = []
            messages = []
            
            socket_.listen(self.max_connections)
            
            self.logger.info( f'Successfully started: {self.listen_address}:{self.listen_port}')
        except Exception as error:
            self.logger.error( f'Error while starting: {error}')
        
        while True:    
            try:
                client, client_address = socket_.accept()
            except OSError:
                pass
            else:
                self.logger.info(f'Connected with {client_address}')
                clients.append(client)

            recv_data_lst = []
            send_data_lst = []
            err_lst = []
            
            try:
                if clients:
                    recv_data_lst, send_data_lst, err_lst = select.select(clients, clients, [], 0)
            except OSError:
                pass
            
            if recv_data_lst:
                for client_with_message in recv_data_lst:
                    try:
                        self.process_client_request(get_message(client_with_message), messages, client_with_message)
                    except:
                        self.logger.info(f'Client {client_with_message.getpeername()} disconnected.')
                        clients.remove(client_with_message)
            
            if messages and send_data_lst:
                message = {
                    ACTION: MESSAGE,
                    SENDER: messages[0][0],
                    TIME: datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    MESSAGE_TEXT: messages[0][1]
                }
                del messages[0]
                for waiting_client in send_data_lst:
                    try:
                        send_message(waiting_client, message)
                    except:
                        self.logger.info(f'Client {waiting_client.getpeername()} disconnected.')
                        clients.remove(waiting_client)

if __name__ == '__main__':
    sr = Server()
    sr.start()
