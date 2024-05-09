# mylib.py
import logging
logger = logging.getLogger(__name__)

def do_something():
    logger.info('Doing something')
    logger.setLevel(level=10)
    logger.debug('a debug info')