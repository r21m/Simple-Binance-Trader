#! /usr/bin/env python3

'''
run

'''
import configparser
import logging

from core import botCore

## Config File Path.
config_file = ("./settings.cfg")
##-------------------->


## Setting up the logger.
logger = logging.getLogger()

formatter = logging.Formatter('%(asctime)s:%(name)s:%(message)s')

file_handler = logging.FileHandler('runtimeLogs.log')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

##

## Runtime management varaiables.
updaterThreadActive = False
coreManThreadActive = False
bot_core = None
##-------------------->

                
def read_config():

    config = configparser.ConfigParser()
    config.read(config_file)

    runType = (config['trader']['runType'])
    mainInterval = (config['trader']['traderCurrency'])
    MAC = float(config['trader']['traderCurrency'])

    if runType is not 'REAL':
        privateKey = None
        publicKey = None
    else:
        publicKey = (config['keys']['publicKey'])
        privateKey = (config['keys']['privateKey'])

    markets = (config['trader']['markets'])
    markets = markets.replace(' ', '')
    markets_trading = markets.split(',')

    if 'debug' in config:
        debugLevel = config['debug']['debugLevel']    
        if debugLevel == 'warning':
            logger.setLevel(logging.WARNING)
        elif debugLevel == 'debug':
            logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)
    return runType, MAC, markets_trading, mainInterval, publicKey, privateKey    

def main():
    '''
    This is where all the data that will be used during runtime is collected.
    -> Setup the botcore.
    -> Setup the terminal feed thread.
    -> Start the botcore.
    '''
    global bot_core

    runType, MAC, markets_trading, mainInterval, publicKey, privateKey = read_config()
    
    print('Starting in {0} mode.'.format(runType.upper()))
    print(runType, MAC, markets_trading, mainInterval, publicKey, privateKey)
    
    ## <----------------------------------| RUNTIME CHECKS |-----------------------------------> ##
    bot_core = botCore.BotCore(runType, MAC, markets_trading, mainInterval, publicKey, privateKey)
    logging.info('Created bot core object.')

    ## <----------------------------------| RUNTIME CHECKS |-----------------------------------> ##
    if bot_core != None:
        bot_core.start()
        logging.info('Started bot core.')
        return

    logging.error('Unable to start collecting.')

if __name__ == '__main__':    
    main()
