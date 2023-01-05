import sys
import os
import logging
import logging.handlers
from common.constants import LOGGING_LEVEL
sys.path.append('../')

_format = logging.Formatter('%(asctime)s %(levelname)s server.py %(message)s')

log_file_name = os.path.dirname(os.path.abspath(__file__))
log_file_name = os.path.join(log_file_name, 'server.log')

stream_handler = logging.StreamHandler(sys.stderr)
stream_handler.setFormatter(_format)
stream_handler.setLevel(logging.CRITICAL)

file_handler = logging.handlers.TimedRotatingFileHandler(log_file_name, encoding='utf8', interval=1, when='D')
file_handler.setFormatter(_format)

logger = logging.getLogger('server')
logger.addHandler(stream_handler)
logger.addHandler(file_handler)
logger.setLevel(LOGGING_LEVEL)

if __name__ == '__main__':
    logger.critical('Критическая ошибка')
    logger.error('Ошибка')
    logger.debug('Отладочная информация')
    logger.info('Информационное сообщение')