from socket import *
from datetime import datetime
import sys

from common.constants import *
from common.utils import *

from decorators import log

import logs.client_log_config
CLIENT_LOGGER = logging.getLogger('client')

@log
def make_presense(account_name='Guest'):
    
    CLIENT_LOGGER.debug(f'Created {PRESENCE}-message for {account_name}')
    
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
def process_ans(response):
    
    CLIENT_LOGGER.debug(f'Processing response from server: {response}')
    
    if RESPONSE in response:
        if response[RESPONSE] == 200:
            return f'Response code: {response[RESPONSE]}\nAlert: {response[ALERT]}'
        return f'Response code: {response[RESPONSE]}\nError: {response[ERROR]}'
    raise Exception

def main():
    try:
        server_address = sys.argv[1]
        server_port = int(sys.argv[2])
        if server_port < 1024 or server_port > 65535:
            raise ValueError
    except IndexError:
        CLIENT_LOGGER.info( f'Set settings to default: {DEFAULT_IP_ADDRESS}:{DEFAULT_PORT}.')
        server_address = DEFAULT_IP_ADDRESS
        server_port = DEFAULT_PORT
    except ValueError:
        CLIENT_LOGGER.critical( f'Undefined port (must be in range from 1024 to 65535): {server_port}.')
        sys.exit(1)
        
    try:
        CLIENT_LOGGER.info( f'Trying to connect to {server_address}:{server_port}.')
        socket_ = socket(AF_INET, SOCK_STREAM)
        socket_.connect((server_address, server_port))
        CLIENT_LOGGER.info( f'Successfully connected to {server_address}:{server_port}.')
        request_to_server = make_presense()
        send_message(socket_, request_to_server)
    except ConnectionRefusedError:
        CLIENT_LOGGER.error(f'Connection refused: {server_address}:{server_port}')
        sys.exit(1)
    except Exception as error:
        CLIENT_LOGGER.error(f'Connection error: {error}:{server_port}')
        sys.exit(1)
        
    try:
        responce = process_ans(get_message(socket_))
        CLIENT_LOGGER.info( f'Get answer from server: {responce}.')
    except Exception as error:
        CLIENT_LOGGER.error(f'Decoding error: {error}')


if __name__ == '__main__':
    main()
