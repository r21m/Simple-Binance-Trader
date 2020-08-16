#! /usr/bin/env python3

'''
run

'''
import configparser
import logging

from core import botCore

## Config File Path.
config_file = ("./settings.cfg")

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

    runType = (config['trader']['run_type'])
    mainInterval = (config['trader']['main_interval'])
    MAC = float(config['trader']['trader_currency'])
    commision_fee = float(config['trader']['commision_fee'])
    native_currency = (config['trader']['native_currency'])

    if runType is not 'REAL':
        privateKey = None
        publicKey = None
        runType = 'TEST'
    else:
        publicKey = (config['keys']['public_key'])
        privateKey = (config['keys']['private_key'])

    markets = (config['trader']['markets'])
    markets = markets.replace(' ', '')
    markets = markets.replace('_', '-')
    markets_trading = markets.split(',')

    if 'debug' in config:
        debugLevel = config['debug']['level']
        if debugLevel == 'warning':
            logger.setLevel(logging.WARNING)
        elif debugLevel == 'debug':
            logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)
    return runType, MAC, markets_trading, mainInterval, publicKey, privateKey, native_currency, commision_fee


def main():
    """
    This is where all the data that will be used during runtime is collected.
    -> Setup the botcore.
    -> Setup the terminal feed thread.
    -> Start the botcore.
    """
    global bot_core

    runType, MAC, markets_trading, mainInterval, publicKey, privateKey, native_currency, fee = read_config()

    print('Starting in {0} mode.'.format(runType.upper()))
    #print(runType, MAC, markets_trading, mainInterval, publicKey, privateKey)

    ## <----------------------------------| RUNTIME CHECKS |-----------------------------------> ##
    bot_core = botCore.BotCore(runType, MAC, markets_trading, mainInterval, publicKey, privateKey, native_currency)
    logging.info('Created bot core object.')

    ## <----------------------------------| RUNTIME CHECKS |-----------------------------------> ##
    if bot_core != None:
        bot_core.start()
        logging.info('Started bot core.')
        return

    logging.error('Unable to start collecting.')

if __name__ == '__main__':
    main()
