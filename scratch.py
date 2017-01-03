# scratch.py
# Author: Steve Dwyer
# Scratch pad for temporary work

import sys, logging, textwrap, cipher_utils
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

def binStrtoDecInt(binStr):
	# Converts a binary representation as a string to a decimal integer
	""" (str) -> integer
	
	Convert a binary representation as a string to a decimal integer
	
	>>> binStrtoDecInt('00111011')
	59
	"""
	
	return int(binStr, base=2)

def integerToChr(cipherInt):
	# Converts a mod 26 integer to a upper case character between A..Z
	""" (integer) -> str
	
	Convert a mod 26 integer to a upper case character between A..Z
	
	>>> integerToChr(7)
	'H'
	"""

	return chr(cipherInt + 65)

def binStrsToCipherText(binStrs):
	# Converts a list of binary representations as strings to a string of upper case characters between A..Z
	""" (list) -> str
	
	Convert a list of binary representations as strings to a string of upper case characters between A..Z
	
	>>> binStrsToCipherText(['10', '00', '00', '01', '00111011', ''])
	CAABH
	"""
	cipherlist = []
	logger.debug('Bin\tInt\tMod26\tChr')
	for binStr in binStrs:
		if binStr != '':
			cipherInt = binStrtoDecInt(binStr)
			moddedCipherInt = cipherInt % 26
			cipherChar = integerToChr(moddedCipherInt)
			logger.debug('%s\t%s\t%s\t%s' % (binStr, cipherInt, moddedCipherInt, cipherChar))
			cipherlist.append(cipherChar)

	return ''.join(cipherlist)

def main():
	print('Ensure that cipherbin.txt is present in the same directory as scratch.py')
	input('Hit any key to continue...')
	print('Reading in file cipherbin.txt and removing all whitespace characters...')
	import cipher_utils
	cipherbintext = cipher_utils.stripWhitespace(cipher_utils.readFile('cipherbin.txt'))
	setLoggingLevel(logging.DEBUG)
	logger.debug('%s' % (cipherbintext))
	cipherbinlist = cipherbintext.split(sep='2')
	cipherbinstrippedtext = ''.join(cipherbinlist)
	cipherbinlist = textwrap.wrap(cipherbinstrippedtext, 5)
	ciphertext = binStrsToCipherText(cipherbinlist)
	logger.info(ciphertext)
	cipher_utils.writeFile('cipher.txt', ciphertext)
	setLoggingLevel(logging.ERROR)

# if scratch.py is run, instead of being imported as a module,
# call the main() function

# Always perform a sanity check first:
print('Checking decryption logic on scratch module...')
setLoggingLevel(logging.ERROR)

if binStrtoDecInt('00111011') != 59:
	print('Error testing binStrtoDecInt(bin) method!!! Check your code before continuing...')
	sys.exit()
elif integerToChr(7) != 'H':
	print('Error testing integerToChr(cipherInt) method!!! Check your code before continuing...')
	sys.exit()
elif binStrsToCipherText(['10', '00', '00', '01', '00111011', '']) != 'CAABH':
	print('Error testing binStrsToCipherText(binStrs) method!!! Check your code before continuing...')
	sys.exit()
else:
	print('decryption logic OK.')

if __name__ == '__main__':
	main()
