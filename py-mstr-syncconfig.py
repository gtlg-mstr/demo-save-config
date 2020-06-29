import logging
from logging.handlers import RotatingFileHandler
from logging import handlers
import sys
import requests, json #For MSTR API ACCESS
#import yaml 
# YAML Intro https://stackabuse.com/reading-and-writing-yaml-to-a-file-in-python/
import configparser
import pandas


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

log.info('reading config file')
##Read config files
Config = configparser.ConfigParser()
Config.read('config.ini')
ConfigSections = Config.sections()

print(ConfigSections)

def ConfigSectionMap(section):
    dict1 = {}
    options = Config.options(section)
    for option in options:
        try:
            dict1[option] = Config.get(section, option)
            if dict1[option] == -1:
                DebugPrint("skip: %s" % option)
        except:
            print("exception on %s!" % option)
            dict1[option] = None
    return dict1

log.info('Checking section')
serverid = ConfigSectionMap("server")['serverid']
base_url='https://env-%s.customer.cloud.microstrategy.com/MicroStrategyLibrary/api/' % serverid
log.info(base_url)
log.info('Getting login and project details and converting to variables')
api_login = ConfigSectionMap("server")['api_login']
api_password = ConfigSectionMap("server")['api_password']
project_id = ConfigSectionMap("server")['project_id']




#### FUNCTIONS ###
#login
def login(base_url,api_login,api_password):
    print("Getting token...")
    data_get = {'username': api_login,
                'password': api_password,
                'loginMode': 1}
    r = requests.post(base_url + 'auth/login', data=data_get)
    if r.ok:
        authToken = r.headers['X-MSTR-AuthToken']
        cookies = dict(r.cookies)
        print("\nToken: " + authToken)
        return authToken, cookies
    else:
        print("HTTP %i - %s, Message %s" % (r.status_code, r.reason, r.text))

#logout
def logout(base_url,api_login,api_password):
    print("Logging out...")
    r = requests.post(base_url + 'auth/logout')
    if r.ok:
        log.info('Successfully logged out of %s' % base_url)
    
    else:
        print("HTTP %i - %s, Message %s" % (r.status_code, r.reason, r.text))

#headers
def set_headers(authToken,project_id):
    headers = {'X-MSTR-AuthToken': authToken,
               'Content-Type': 'application/json',#IMPORTANT!
               'Accept': 'application/json',
               'X-MSTR-ProjectID': project_id}
    return headers