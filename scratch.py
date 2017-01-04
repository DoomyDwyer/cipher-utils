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

def baconianBinToText(binStrs, sep=''):
	# Converts a list of Baconian binary (blocksize 5) strings to a string
	""" (list, str sep='') -> str
	
	Convert a list of Baconian binary (blocksize 5) strings to a string of upper case characters between A..Z
	If sep is not given, the string returned will be one contigious block of characters, otherwise the 'words'
	be be separated by the character sep
	
	>>> baconianBinToText(['10', '00', '00', '01', '00'])
	BI
	"""
	cipherlist = []
	logger.debug('Bin\tInt\tMod26\tChr')
	position = 0
	while position < len(binStrs):
		for column in range(len(binStrs[position])):
			#binStr = binStrs[position][column] + binStrs[position+1][column] + binStrs[position+2][column] + binStrs[position+3][column] + binStrs[position+4][column]
			binStr = binStrs[position+4][column] + binStrs[position+3][column] + binStrs[position+2][column] + binStrs[position+1][column] + binStrs[position][column]
			cipherInt = binStrtoDecInt(binStr)
			moddedCipherInt = cipherInt % 26
			cipherChar = integerToChr(moddedCipherInt)
			modded = ''
			if cipherInt != moddedCipherInt:
				modded = ' - modded!'
			logger.debug('%s\t%s\t%s\t%s\t%s' % (binStr, cipherInt, moddedCipherInt, cipherChar, modded))
			cipherlist.append(cipherChar)
		position+=5
		cipherlist.append(sep)
	return ''.join(cipherlist)

def main():
	print('Ensure that cipherbin.txt is present in the same directory as scratch.py')
	input('Hit any key to continue...')
	print('Reading in file cipherbin.txt and removing all whitespace characters...')
	import cipher_utils
	cipherbintext = cipher_utils.stripWhitespace(cipher_utils.readFile('cipherbin.txt'))
	setLoggingLevel(logging.ERROR)
	logger.debug('%s' % (cipherbintext))
	cipherbinlist = cipherbintext.split(sep='2')
	print(cipherbinlist)
	input('Hit any key to continue...')
	ciphertext = baconianBinToText(cipherbinlist, sep=' ')
	logger.info(ciphertext)
	cipher_utils.writeFile('cipher.txt', ciphertext)
	print('Let\'s perform some frequency analysis on the ciphertext we extracted from the Baconian binary text...')
	input('Hit any key to continue...')
	setLoggingLevel(logging.ERROR)
	ciphertext = cipher_utils.stripWhitespace(cipher_utils.readFile('cipher.txt'))
	cipherlist=list(ciphertext)
	freq = cipher_utils.frequencyAnalysis(cipherlist)
	sortedFreq = cipher_utils.sortedFrequency(freq)
	cipher_utils.displayFrequency(sortedFreq)
	print('ioc = %s' % (cipher_utils.ioc(cipherlist)))
	print('Let\'s decrypt the ciphertext using the Simple Substitution Cipher decryption algorithm, with our guessed key...')
	input('Hit any key to continue...')
	ciphertext = cipher_utils.readFile('cipher.txt')
	setLoggingLevel(logging.DEBUG)
	plaintext = cipher_utils.decryptSimpleSubstitutionCipher(ciphertext, 'DIJAKLMNFOPQECRSTUVWXYZGBH', dummy='.')
	print(plaintext)
	cipher_utils.writeFile('solution.txt', plaintext)
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
elif baconianBinToText(['10', '00', '00', '01', '00']) != 'BI':
	print('Error testing baconianBinToText(binStrs) method!!! Check your code before continuing...')
	sys.exit()
else:
	print('decryption logic OK.')

if __name__ == '__main__':
	main()
