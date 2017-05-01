# logger.py
# Author: Steve Dwyer
# Changes:
#   1 May 2017:
#   Support environments where the python logging module isn't available, such as trinket:
#   Custom implementation created to avoid dependency on other python modules
#   This version will print to the console exclusively

import time

# Levels
from enum import IntEnum
class Level(IntEnum):
	ALL = 0
	DEBUG = 1
	INFO = 2
	WARN = 3
	ERROR = 4

# The actual Logger class
class Logger:
	"""
	The implmentation of a console only Logger, which works independently of the pythong logging module
	"""
	
	def __init__(self, level):
		"""
		Constructs a new instance of Logger, with the logging level set to level
		"""
		self.level = level
	
	def setLevel(self, level):
		"""
		Sets the logging level set to level
		"""
		self.level = level
	
	def debug(self, msg):
		if self.level <= Level.DEBUG:
			print('%s - %s - %s' % (time.asctime(), Level.DEBUG.name, msg))
	
	def info(self, msg):
		if self.level <= Level.INFO:
			print('%s - %s - %s' % (time.asctime(), Level.INFO.name, msg))
	
	def warn(self, msg):
		if self.level <= Level.WARN:
			print('%s - %s - %s' % (time.asctime(), Level.WARN.name, msg))
	
	def error(self, msg):
		if self.level <= Level.ERROR:
			print('%s - %s - %s' % (time.asctime(), Level.ERROR.name, msg))

def getLogger():
	"""
	Factory method for creating a new instance of Logger, and initialising
	its logging level to 0 (all)
	"""
	return Logger(Level.ALL)

def setLoggingLevel(level):
	"""
	Sets the logging level
	"""
	logger.setLevel(level)

def debug(msg):
	logger.debug(msg)

def info(msg):
	logger.info(msg)

def warn(msg):
	logger.warn(msg)

def error(msg):
	logger.error(msg)

logger = getLogger()
#logger = Logger(Level.ALL)
