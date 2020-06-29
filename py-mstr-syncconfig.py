import logging
from logging.handlers import RotatingFileHandler
from logging import handlers
import sys
import requests, json #For MSTR API ACCESS
import yaml 


#set logging level
## Use filename as variale
## Sets level to INFO and sets format to be used for file and console
log = logging.getLogger(__name__) 
log.setLevel(logging.INFO)
format = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

# Set logging to Console
ch = logging.StreamHandler(sys.stdout)
ch.setFormatter(format)
log.addHandler(ch)

# Set logging to file, with size and rotation
fh = handlers.RotatingFileHandler('logfile2.log', maxBytes=(1048576*5), backupCount=7)
fh.setFormatter(format)
log.addHandler(fh)

# Logs test
# log.debug('A debug message')
# log.info('An info message')
# log.warning('Something is not right.')
# log.error('A Major error has happened.')
# log.critical('Fatal error. Cannot continue')

