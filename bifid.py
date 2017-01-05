# bifid.py
# Author: Steve Dwyer

import sys, logging, cipher_utils
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

def encryptBifid(charList, keyString, period):
	""" (list, str, int) -> str
	
	Encrypt the passed plaintext list charList with the Bifid cipher
	using the passed key keyString and period period.
	
	>>> encryptBifid('thisissecret', 'IULESABCDFGHKMNOPQRTVWXYZ', 4)
	XXX
	"""

def decryptBifid(charList, keyString, period):
	""" (list, str, int) -> str
	
	Decrypt the passed ciphertext list charList, encrypted with the Bifid cipher
	using the passed key keyString and period period.
	
	>>> decryptBifid('XXX', 'IULESABCDFGHKMNOPQRTVWXYZ', 4)
	thisissecret
	"""


# if bifid.py is run, instead of being imported as a module,
# call the main() function

# Always perform a sanity check first on the known example cipher:
print('Checking decryption logic on bifid module...')
setLoggingLevel(logging.ERROR)
#if decryptBifid(['A', 'B', 'C'], 'KEYABCDFGHIJLMNOPQRSTUVWXZ', 4) != 'key':
#	print('Error testing decryptBifid(charList, keyString) method!!! Check your code before continuing...')
#	sys.exit()
else:
	print('decryption logic OK.')

if __name__ == '__main__':
	main()
