import itertools
import time
from datetime import datetime
from functools import wraps
from logging import getLogger

logger = getLogger("load_attack_surface_data")

def remove_duplication(items: list) -> list:
    """
        :return: A list with no duplications
    """
    return list(set(items))


def flatten(list_of_lists: list) -> list:
    return list(itertools.chain.from_iterable(list_of_lists))


def get_print_name(f):
    """
    :param tuple args: Use the args of the function to figure
     a nice pretty name of the function which this args belong to.
    :rtype: str
    """

    # The first param of the args is the self which in most cases we can get a nice name from.
    print_name = f.__name__

    return print_name


def log_runtime_duration(f):
    """
    a decorator to print the time the function execution took and how long it has been since the function was last
    called
    """

    @wraps(f)
    def wrap(*args):
        start_time = time.time()

        module_name = get_print_name(f)

        logger.info(f"{datetime.now()} entering [{module_name}]")
        
        ret = f(*args)
        end_time = time.time()
        runtime_duration_ms = round((end_time - start_time) * 1000.0)
        logger.info(f"{datetime.now()} exiting [{module_name}] took {runtime_duration_ms} ms")
        return ret

    return wrap
