# logger.py
# Author: Steve Dwyer

import logging

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
consoleHandler = logging.StreamHandler()
consoleHandler.setLevel(logging.ERROR)
consoleHandler.setFormatter(formatter)
logger.addHandler(consoleHandler)

def setLoggingLevel(level):
	# Sets the logging level
	consoleHandler.setLevel(level)

def debug(msg):
	logger.debug(msg)

def info(msg):
	logger.info(msg)

def error(msg):
	logger.error(msg)
