import sys
import logging
import logs.client_log_config
import logs.server_log_config
import inspect
from functools import wraps

if sys.argv[0].find('client') == -1:
    LOGGER = logging.getLogger('server')
else:
    LOGGER = logging.getLogger('client')

def log(func_to_log):
    @wraps(func_to_log)
    def log_saver(*args, **kwargs):
        ret = func_to_log(*args, **kwargs)
        LOGGER.info(f'Function <{func_to_log.__name__}> was called from <{inspect.stack()[1][3]}> function')
        return ret
    return log_saver

