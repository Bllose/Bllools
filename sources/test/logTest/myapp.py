# myapp.py
import logging
from test.logTest.lib import mylib

logger = logging.getLogger(__name__)

def main():
    FORMAT = '%(asctime)s %(levelname)-10s %(name)-30s %(message)s'
    logging.basicConfig(format=FORMAT, level=logging.INFO)
    logger.info('Started2')
    mylib.do_something()
    logger.info('Finished2')
    logging.warning('a warning info')
    logger.debug('an other debug info')

    

if __name__ == '__main__':
    main()