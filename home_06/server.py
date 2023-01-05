from socket import *
import sys

from common.constants import *
from common.utils import *

import logging
import logs.server_log_config

from decorators import log

SERVER_LOGGER = logging.getLogger('server')

@log
def process_client_request(request):
    
    SERVER_LOGGER.info('Processing client request')
    
    if ACTION in request and request[ACTION] == PRESENCE and TIME in request and USER in request and request[USER].get(ACCOUNT_NAME) == 'Guest':
        SERVER_LOGGER.info('Succsessfully processed')
        return {RESPONSE: 200,
                ALERT: 'Connected'}
    SERVER_LOGGER.info('Bad request processed')
    return {
        RESPONSE: 400,
        ERROR: 'Bad Request'
    }

def main():
    try:
        if '-p' in sys.argv:
            listen_port = int(sys.argv[sys.argv.index('-p') + 1])
        else:
            SERVER_LOGGER.info( f'Port set to default {DEFAULT_PORT}')
            listen_port = DEFAULT_PORT
        if listen_port < 1024 or listen_port > 65535:
            raise Exception
    except IndexError:
        SERVER_LOGGER.error( f'Invalid port (-p) input (must be in range from 1024 to 65535) while starting')
        sys.exit(1)

    try:
        if '-a' in sys.argv:
            listen_address = sys.argv[sys.argv.index('-a') + 1]
        else:
            listen_address = ''
            SERVER_LOGGER.info( f'Adress set to default {DEFAULT_IP_ADDRESS}')
    except Exception:
        SERVER_LOGGER.error( f'Invalid adress (-a) input while starting')
        print('Enter the value of adress (-a)')
        sys.exit(1)

    try:
        SERVER_LOGGER.info( f'Trying to start server: {DEFAULT_IP_ADDRESS}:{DEFAULT_PORT}')
        socket_ = socket(AF_INET, SOCK_STREAM)
        socket_.bind((listen_address, listen_port))
        socket_.listen(MAX_CONNECTIONS)
        SERVER_LOGGER.info( f'Successfully started: {DEFAULT_IP_ADDRESS}:{DEFAULT_PORT}')
    except Exception as error:
        SERVER_LOGGER.error( f'Error while starting: {error}')
    while True:
        client, client_address = socket_.accept()
        try:
            request_from_client = get_message(client)
            SERVER_LOGGER.info( f'{request_from_client[USER][ACCOUNT_NAME]} connected')
            response = process_client_request(request_from_client)
            send_message(client, response)
            client.close()
        except Exception as error:
            SERVER_LOGGER.error( f'Error while processing message: {error}')
            client.close()


if __name__ == '__main__':
    main()
