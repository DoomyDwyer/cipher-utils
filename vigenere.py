# vigenere.py
# Author: Steve Dwyer
#TODO Fix Vigenere cipher (A=0, not 1)

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

def createSubList(charList, k):
	""" (list, integer) -> list
	Return the sublist of charList, containing every kth character (starting at position 0)
	
	>>> createSubList(['X', 'S', 'F', 'J', 'D', 'J', 'M', 'N', 'R', 'F', 'R', 'U', 'D', 'J', 'V', 'L', 'M', 'Y', 'F', 'T', 'G', 'W', 'W', 'H', 'P', 'T', 'U', 'D', 'I', 'A', 'H', 'W', 'R', 'M', 'S', 'X', 'X', 'A', 'H', 'J', 'D', 'N', 'B', 'R', 'H', 'Q', 'T', 'O', 'F', 'F', 'N', 'W', 'F', 'G', 'H', 'G', 'L', 'D', 'J', 'J', 'A', 'T', 'Q', 'W', 'H', 'U', 'E', 'Q', 'E', 'M', 'D', 'M', 'H', 'R', 'H', 'L', 'M', 'C', 'G', 'L', 'Z', 'A', 'Y', 'B', 'T', 'H', 'U', 'W', 'I', 'C', 'M', 'H', 'D', 'J', 'I', 'C', 'G', 'F', 'V', 'Z', 'T', 'J', 'H', 'W', 'R', 'F', 'Y', 'B', 'X', 'B', 'H', 'T', 'T', 'L', 'X', 'A', 'H', 'F', 'L', 'Y', 'M', 'H', 'D', 'K', 'M', 'Z', 'K', 'T', 'P', 'S', 'S', 'U', 'M', 'R', 'H', 'F', 'H', 'L', 'R', 'U', 'W', 'A', 'T', 'H', 'U', 'J', 'V', 'L', 'T', 'Q', 'L', 'Z', 'S', 'G', 'S', 'N', 'A', 'F', 'W', 'L', 'W', 'U', 'G', 'X', 'D', 'U', 'Y', 'C', 'H', 'S', 'W', 'Z', 'J', 'W', 'H', 'S', 'I', 'A', 'I', 'Y', 'G', 'Y', 'L', 'S', 'Q', 'C', 'M', 'D', 'D', 'F', 'I', 'M', 'X', 'H', 'X', 'J', 'N', 'N', 'R', 'Y', 'R', 'E', 'F', 'E', 'X', 'N', 'W', 'H', 'T', 'M', 'L', 'N', 'E', 'D', 'J', 'C', 'Y', 'D', 'R', 'M', 'H', 'I', 'G', 'X', 'L', 'V', 'J', 'L', 'X', 'Q', 'H', 'U', 'Y', 'L', 'H', 'S', 'L', 'U', 'Y', 'L', 'T', 'S', 'V', 'S', 'H', 'N', 'B', 'T', 'Q', 'K', 'F', 'H', 'W', 'T', 'Q', 'D', 'N', 'H', 'X', 'U', 'D', 'Q', 'R', 'Y', 'G', 'Y', 'V', 'S', 'Q', 'F', 'M', 'M', 'R', 'K', 'J', 'Q', 'H', 'Z', 'O', 'V', 'S', 'I', 'M', 'G', 'H', 'H', 'T', 'M', 'L', 'N', 'E', 'D', 'J', 'Q', 'B', 'Y', 'K', 'G', 'Z', 'N', 'X', 'S', 'F', 'J', 'D', 'J', 'M', 'N', 'R', 'F', 'X', 'U', 'B', 'I', 'G', 'J', 'R', 'U', 'K', 'P', 'P', 'S', 'S', 'O', 'E', 'N', 'V', 'S', 'X', 'Y', 'G', 'N', 'R', 'J', 'Q', 'Y', 'V', 'Y', 'X', 'J', 'J', 'L', 'B', 'S', 'F', 'J', 'D', 'J', 'M', 'T', 'J', 'J', 'F', 'J', 'A', 'D', 'D', 'L', 'Y', 'B', 'X', 'Z', 'Q', 'A', 'A', 'Y', 'K', 'X', 'L', 'L', 'D', 'I', 'Y', 'X', 'X', 'J', 'W', 'Y', 'R', 'F', 'W', 'A', 'Y', 'M', 'L', 'N', 'P', 'H', 'Q', 'Y', 'L', 'Y', 'H', 'F', 'H', 'L', 'R', 'U', 'W', 'A', 'T', 'H', 'B', 'X', 'D', 'D', 'Q', 'U', 'U', 'T', 'X', 'L', 'Y', 'L', 'T', 'S', 'V', 'X', 'T', 'L', 'F', 'N', 'Q', 'Y', 'N', 'H', 'M', 'J', 'O', 'D', 'N', 'A', 'B', 'G', 'O', 'W', 'S', 'O', 'F', 'G', 'H', 'J', 'X', 'I', 'K', 'Y', 'H', 'P', 'Y', 'M', 'H', 'Z', 'Q', 'V', 'X', 'U', 'G', 'I', 'L', 'E', 'F', 'A', 'X', 'X', 'L', 'F', 'Y', 'I', 'T', 'X', 'W', 'J', 'J', 'U', 'F', 'T', 'I', 'F', 'T', 'H', 'L', 'J', 'Q', 'K', 'J', 'N', 'A', 'J', 'U', 'W', 'F', 'L', 'X', 'R', 'D', 'F', 'D', 'G', 'T', 'S', 'B', 'O', 'F', 'S', 'L', 'Y', 'R', 'H', 'J', 'L', 'Y', 'T', 'U', 'E', 'Y', 'B', 'T', 'Y', 'W', 'J', 'F', 'H', 'L', 'K', 'R', 'J', 'R', 'U', 'M', 'N', 'R', 'F', 'X', 'I', 'F', 'J', 'V', 'L', 'W', 'U', 'B', 'L', 'K', 'L', 'K', 'I', 'K', 'B', 'D', 'J', 'I', 'U', 'G', 'I', 'V', 'G', 'R', 'Y', 'O', 'J', 'U', 'Q', 'H', 'I', 'F', 'U', 'O', 'W', 'C', 'G', 'H', 'X', 'W', 'A', 'S', 'P', 'H', 'Q', 'Y', 'W', 'X', 'Q', 'T', 'U', 'S', 'A', 'S', 'A', 'E', 'J', 'W', 'L', 'J', 'L', 'L', 'K', 'R', 'J', 'S', 'O', 'F', 'G', 'H', 'J', 'X', 'U', 'G', 'I', 'X', 'K', 'J', 'G', 'T', 'Y', 'K', 'K', 'Y', 'I', 'W', 'T', 'W', 'Z', 'J', 'N', 'K', 'F', 'Q', 'K', 'K', 'I', 'K', 'R', 'D', 'L', 'N', 'I', 'G', 'M', 'R', 'O', 'J', 'P', 'X', 'W', 'Q', 'G', 'R', 'U', 'M', 'Y', 'H', 'J', 'B', 'B', 'B', 'H', 'K', 'E', 'J', 'N', 'A', 'T', 'G', 'A', 'X', 'O', 'L', 'J', 'G', 'L', 'M', 'Y', 'K', 'J', 'V', 'M', 'Q', 'N', 'B', 'S', 'J', 'K', 'H', 'L', 'T', 'R', 'E', 'D', 'J', 'X', 'W', 'F', 'W', 'S', 'X', 'N', 'K', 'J', 'D', 'E', 'X', 'B', 'H', 'Z', 'O', 'V', 'L', 'C', 'O', 'J', 'Q', 'G', 'M', 'C', 'G', 'Y', 'V', 'S', 'G', 'I', 'N', 'Y', 'K', 'G', 'B', 'C', 'M', 'B', 'D', 'K', 'J', 'H', 'V', 'W', 'B', 'H', 'Y', 'Y', 'W', 'I', 'X', 'J', 'N', 'H', 'Z', 'B', 'R', 'J', 'Q', 'X', 'P', 'F', 'U', 'A', 'N', 'N', 'A', 'J', 'D', 'D', 'Q', 'C', 'X', 'X', 'V', 'U', 'T', 'L', 'X', 'I', 'V', 'G', 'R', 'Y', 'G', 'T', 'W', 'S', 'G', 'F', 'X', 'A', 'L', 'U', 'Y', 'I', 'K', 'N', 'H', 'K', 'F', 'A', 'T', 'N', 'Q', 'K', 'Y', 'N', 'A', 'J', 'J', 'W', 'W', 'G', 'T', 'S', 'V', 'T', 'J', 'W', 'T', 'Z', 'V', 'W', 'Y', 'B', 'X', 'N', 'U', 'W', 'S', 'W', 'K', 'D', 'S', 'L', 'N', 'I', 'G', 'X', 'B', 'K', 'Y', 'Y', 'F', 'X', 'G', 'A', 'I', 'H', 'H', 'Y', 'V', 'M', 'K', 'Z', 'B', 'H', 'L', 'W', 'S', 'N', 'E', 'D', 'V', 'U', 'W', 'U', 'F', 'G', 'O', 'W', 'R', 'Y', 'L', 'X', 'D', 'Y', 'J', 'M', 'K', 'N', 'J', 'G', 'W', 'I', 'N', 'X', 'P', 'S', 'Y', 'B', 'X', 'R', 'D', 'L', 'N', 'W', 'T', 'Q', 'D', 'F', 'F', 'F', 'R', 'X', 'L', 'K', 'G', 'S', 'T', 'Q', 'O', 'A', 'J', 'X', 'V', 'T', 'G', 'W', 'H', 'L', 'T', 'H', 'N', 'W', 'W', 'M', 'E', 'F', 'L', 'V', 'G', 'U', 'K', 'J', 'S', 'S', 'Y', 'N', 'X', 'W', 'Q', 'K', 'M', 'C', 'W', 'I', 'H', 'F', 'B', 'C', 'M', 'M', 'L', 'F', 'Y', 'B', 'X', 'R', 'H', 'K', 'X', 'U', 'Z', 'J', 'V', 'S', 'S', 'X', 'N', 'X', 'H', 'V', 'Y', 'B', 'X', 'R', 'W', 'G', 'W', 'Y', 'V', 'W', 'H', 'S', 'Y', 'Y', 'M', 'M', 'H', 'E', 'F', 'W', 'A', 'N', 'Q', 'W', 'Z', 'M', 'X', 'I', 'W', 'G', 'J', 'H', 'V', 'W', 'B', 'H', 'Y', 'N', 'A', 'J', 'P', 'L', 'M', 'I', 'L', 'J', 'F', 'G', 'I', 'Y', 'L', 'W', 'H', 'N', 'T', 'F', 'O', 'J', 'G', 'S', 'W', 'I', 'N', 'S', 'G', 'L', 'M', 'Y', 'N', 'X', 'H', 'G', 'K', 'M', 'X', 'H', 'U', 'W', 'Y', 'E', 'X', 'D', 'V', 'L', 'M', 'U', 'M', 'B', 'H', 'J', 'J', 'M', 'A', 'F', 'U', 'W', 'I', 'U', 'F', 'T', 'Q', 'Y', 'Y', 'B', 'H', 'X', 'H', 'O', 'M', 'I', 'G', 'J', 'H', 'V', 'J', 'X', 'M', 'T', 'F', 'G', 'R', 'G', 'N', 'S', 'L', 'U', 'F', 'N', 'X', 'X', 'H', 'U', 'Z', 'L', 'X', 'Q', 'B', 'L', 'M', 'Y', 'L', 'J', 'D', 'J', 'J', 'E', 'G', 'T', 'Z', 'F', 'F', 'M', 'L', 'D', 'P', 'E', 'J', 'N', 'K', 'N', 'F', 'W', 'S', 'W', 'K', 'D', 'S', 'L', 'N', 'I', 'G', 'X', 'B', 'K', 'Y', 'Y', 'F', 'X', 'D', 'F', 'I', 'B', 'T', 'A', 'H', 'S', 'B', 'Y', 'T', 'P', 'Q', 'W', 'X', 'M', 'B', 'S', 'W', 'Z', 'F', 'N', 'X', 'A', 'H', 'J', 'D', 'I', 'G', 'J', 'L', 'F', 'A', 'I', 'E', 'A', 'H', 'V', 'M', 'U', 'L', 'Y', 'R', 'H', 'T', 'M', 'L', 'J', 'V', 'K', 'Y', 'B', 'X', 'X', 'D', 'E', 'J', 'M', 'X', 'Y', 'R', 'X', 'X', 'Y', 'V', 'W', 'H', 'L', 'P', 'Y', 'R', 'X'], 6)
	['X', 'M', 'D', 'F', 'P', 'H', 'X', 'B', 'F', 'H', 'A', 'E', 'H', 'G', 'T', 'M', 'G', 'H', 'X', 'X', 'M', 'K', 'M', 'R', 'U', 'L', 'A', 'G', 'H', 'H', 'G', 'M', 'X', 'R', 'X', 'L', 'Y', 'G', 'X', 'H', 'T', 'B', 'W', 'X', 'G', 'M', 'H', 'M', 'L', 'B', 'X', 'M', 'B', 'K', 'E', 'G', 'V', 'B', 'M', 'A', 'X', 'K', 'Y', 'R', 'L', 'L', 'R', 'B', 'U', 'T', 'F', 'M', 'B', 'F', 'K', 'H', 'G', 'X', 'T', 'F', 'L', 'A', 'X', 'T', 'L', 'Y', 'T', 'L', 'M', 'F', 'B', 'K', 'G', 'O', 'F', 'H', 'H', 'T', 'E', 'L', 'F', 'G', 'T', 'W', 'K', 'K', 'G', 'X', 'M', 'B', 'A', 'L', 'K', 'B', 'T', 'W', 'K', 'H', 'O', 'G', 'N', 'M', 'V', 'W', 'Z', 'P', 'A', 'X', 'X', 'G', 'X', 'K', 'T', 'A', 'T', 'T', 'X', 'K', 'G', 'F', 'H', 'B', 'E', 'F', 'L', 'K', 'N', 'X', 'T', 'R', 'T', 'V', 'T', 'E', 'K', 'X', 'W', 'M', 'X', 'Z', 'N', 'X', 'V', 'M', 'A', 'X', 'V', 'A', 'L', 'L', 'O', 'N', 'N', 'X', 'X', 'M', 'A', 'F', 'H', 'G', 'M', 'N', 'X', 'X', 'L', 'G', 'L', 'K', 'K', 'G', 'F', 'T', 'T', 'B', 'X', 'G', 'E', 'L', 'L', 'X', 'X', 'V', 'R']
	"""
	n = len(charList)
	subListIndex = 0
	done = False
	subList = []
	while not done:
		subList.append(charList[subListIndex])
		subListIndex += k
		if subListIndex >= n:
			done = True
	logger.info('\t\tk=%s : chars = %s' % (k, ''.join(subList)))
	return subList

def displayIocTable(charList, maxKeyLength):
	# Displays a list of iocs for each possible key length,
	# from 1 (Simple Caesar Shift) to maxKeyLength
	print('k\tioc')
	print('=\t===')
	for k in range(1, maxKeyLength+1):
		subList = createSubList(charList, k)
		iocK = cipher_utils.ioc(subList)
		print('%s\t%s' % (k, iocK))

def displaySubkeyFrequencies(charList, keyLength):
	# Displays a sorted list of the frequency for each subkey, with key length keyLength
	for index in range(0, keyLength):
		subList = createSubList(charList[index:], keyLength)
		freq = cipher_utils.frequencyAnalysis(subList)
		sortedFreq = cipher_utils.sortedFrequency(freq)
		print('Frequency Analysis for subkey %s' % (index+1))
		cipher_utils.displayFrequency(sortedFreq)

def deriveVigenereKeyPhraseFromCrib(cipherChars, crib):
	# Derive a possible Vigenere keyphrase from the most frequently occurring letter for each sub key
	""" (str, str) -> str
	
	Derive a possible Vigenere keyphrase from a section of the cipher, with a guessed crib
	
	>>> deriveVigenereKeyPhrase('HTPEG', 'MARTIN')
	'MARTIN'
	"""
	keyPhrase = []
	index = 0
	for cipherChar in cipherChars:
		cipherCharOrdinal = cipher_utils.cipherLetterToOrdinal(cipherChar)
		caesarShift = (cipherCharOrdinal - cipher_utils.cipherLetterToOrdinal(crib[index]) - 1) % 26
		keyChar = cipher_utils.ordinalToClearLetter(caesarShift).upper()
		keyPhrase.append(keyChar)
		logger.info('Cipher character %s (%s) should be %s (%s),\tCaesar Shift for sub key = %s,\tkeyChar = %s' % (cipherChar, cipherCharOrdinal+1, crib[index], cipherLetterToOrdinal(crib[index]) + 1, caesarShift+1, keyChar))
		index += 1
	return ''.join(keyPhrase)

def deriveVigenereKeyPhrase(frequentChars):
	# Derive a possible Vigenere keyphrase from the most frequently occurring letter for each sub key
	""" (str) -> str
	
	Derive a possible Vigenere keyphrase from the most frequently occurring letter for each sub key
	Please note, the key length should be known, or at least correctly guessed, for this function
	to produce meaningful results.
	
	>>> deriveVigenereKeyPhrase('XJHJDY')
	'SECRET'
	"""
	keyPhrase = []
	for frequentChar in frequentChars:
		frequentCharOrdinal = cipher_utils.cipherLetterToOrdinal(frequentChar)
		caesarShift = (frequentCharOrdinal - 5) % 26 # 'E' = 5
		keyChar = cipher_utils.ordinalToClearLetter(caesarShift).upper()
		keyPhrase.append(keyChar)
		logger.info('Frequent character %s (%s) should be E (5),\tCaesar Shift for sub key = %s,\tkeyChar = %s' % (frequentChar, frequentCharOrdinal+1, caesarShift+1, keyChar))
	return ''.join(keyPhrase)

def decryptVigenere(charList, keyString):
	""" (list, str) -> str
	
	Decrypt the passed ciphertext list charList, encrypted with the Vigenere cipher
	using the passed key keyString.
	
	>>> decryptVigenere(['X', 'S', 'F', 'J', 'D', 'J', 'M', 'N', 'R', 'F', 'R', 'U', 'D', 'J', 'V', 'L', 'M', 'Y', 'F', 'T', 'G', 'W', 'W', 'H', 'P', 'T', 'U', 'D', 'I', 'A', 'H', 'W', 'R', 'M', 'S', 'X', 'X', 'A', 'H', 'J', 'D', 'N', 'B', 'R', 'H', 'Q', 'T', 'O', 'F', 'F', 'N', 'W', 'F', 'G', 'H', 'G', 'L', 'D', 'J', 'J', 'A', 'T', 'Q', 'W', 'H', 'U', 'E', 'Q', 'E', 'M', 'D', 'M', 'H', 'R', 'H', 'L', 'M', 'C', 'G', 'L', 'Z', 'A', 'Y', 'B', 'T', 'H', 'U', 'W', 'I', 'C', 'M', 'H', 'D', 'J', 'I', 'C', 'G', 'F', 'V', 'Z', 'T', 'J', 'H', 'W', 'R', 'F', 'Y', 'B', 'X', 'B', 'H', 'T', 'T', 'L', 'X', 'A', 'H', 'F', 'L', 'Y', 'M', 'H', 'D', 'K', 'M', 'Z', 'K', 'T', 'P', 'S', 'S', 'U', 'M', 'R', 'H', 'F', 'H', 'L', 'R', 'U', 'W', 'A', 'T', 'H', 'U', 'J', 'V', 'L', 'T', 'Q', 'L', 'Z', 'S', 'G', 'S', 'N', 'A', 'F', 'W', 'L', 'W', 'U', 'G', 'X', 'D', 'U', 'Y', 'C', 'H', 'S', 'W', 'Z', 'J', 'W', 'H', 'S', 'I', 'A', 'I', 'Y', 'G', 'Y', 'L', 'S', 'Q', 'C', 'M', 'D', 'D', 'F', 'I', 'M', 'X', 'H', 'X', 'J', 'N', 'N', 'R', 'Y', 'R', 'E', 'F', 'E', 'X', 'N', 'W', 'H', 'T', 'M', 'L', 'N', 'E', 'D', 'J', 'C', 'Y', 'D', 'R', 'M', 'H', 'I', 'G', 'X', 'L', 'V', 'J', 'L', 'X', 'Q', 'H', 'U', 'Y', 'L', 'H', 'S', 'L', 'U', 'Y', 'L', 'T', 'S', 'V', 'S', 'H', 'N', 'B', 'T', 'Q', 'K', 'F', 'H', 'W', 'T', 'Q', 'D', 'N', 'H', 'X', 'U', 'D', 'Q', 'R', 'Y', 'G', 'Y', 'V', 'S', 'Q', 'F', 'M', 'M', 'R', 'K', 'J', 'Q', 'H', 'Z', 'O', 'V', 'S', 'I', 'M', 'G', 'H', 'H', 'T', 'M', 'L', 'N', 'E', 'D', 'J', 'Q', 'B', 'Y', 'K', 'G', 'Z', 'N', 'X', 'S', 'F', 'J', 'D', 'J', 'M', 'N', 'R', 'F', 'X', 'U', 'B', 'I', 'G', 'J', 'R', 'U', 'K', 'P', 'P', 'S', 'S', 'O', 'E', 'N', 'V', 'S', 'X', 'Y', 'G', 'N', 'R', 'J', 'Q', 'Y', 'V', 'Y', 'X', 'J', 'J', 'L', 'B', 'S', 'F', 'J', 'D', 'J', 'M', 'T', 'J', 'J', 'F', 'J', 'A', 'D', 'D', 'L', 'Y', 'B', 'X', 'Z', 'Q', 'A', 'A', 'Y', 'K', 'X', 'L', 'L', 'D', 'I', 'Y', 'X', 'X', 'J', 'W', 'Y', 'R', 'F', 'W', 'A', 'Y', 'M', 'L', 'N', 'P', 'H', 'Q', 'Y', 'L', 'Y', 'H', 'F', 'H', 'L', 'R', 'U', 'W', 'A', 'T', 'H', 'B', 'X', 'D', 'D', 'Q', 'U', 'U', 'T', 'X', 'L', 'Y', 'L', 'T', 'S', 'V', 'X', 'T', 'L', 'F', 'N', 'Q', 'Y', 'N', 'H', 'M', 'J', 'O', 'D', 'N', 'A', 'B', 'G', 'O', 'W', 'S', 'O', 'F', 'G', 'H', 'J', 'X', 'I', 'K', 'Y', 'H', 'P', 'Y', 'M', 'H', 'Z', 'Q', 'V', 'X', 'U', 'G', 'I', 'L', 'E', 'F', 'A', 'X', 'X', 'L', 'F', 'Y', 'I', 'T', 'X', 'W', 'J', 'J', 'U', 'F', 'T', 'I', 'F', 'T', 'H', 'L', 'J', 'Q', 'K', 'J', 'N', 'A', 'J', 'U', 'W', 'F', 'L', 'X', 'R', 'D', 'F', 'D', 'G', 'T', 'S', 'B', 'O', 'F', 'S', 'L', 'Y', 'R', 'H', 'J', 'L', 'Y', 'T', 'U', 'E', 'Y', 'B', 'T', 'Y', 'W', 'J', 'F', 'H', 'L', 'K', 'R', 'J', 'R', 'U', 'M', 'N', 'R', 'F', 'X', 'I', 'F', 'J', 'V', 'L', 'W', 'U', 'B', 'L', 'K', 'L', 'K', 'I', 'K', 'B', 'D', 'J', 'I', 'U', 'G', 'I', 'V', 'G', 'R', 'Y', 'O', 'J', 'U', 'Q', 'H', 'I', 'F', 'U', 'O', 'W', 'C', 'G', 'H', 'X', 'W', 'A', 'S', 'P', 'H', 'Q', 'Y', 'W', 'X', 'Q', 'T', 'U', 'S', 'A', 'S', 'A', 'E', 'J', 'W', 'L', 'J', 'L', 'L', 'K', 'R', 'J', 'S', 'O', 'F', 'G', 'H', 'J', 'X', 'U', 'G', 'I', 'X', 'K', 'J', 'G', 'T', 'Y', 'K', 'K', 'Y', 'I', 'W', 'T', 'W', 'Z', 'J', 'N', 'K', 'F', 'Q', 'K', 'K', 'I', 'K', 'R', 'D', 'L', 'N', 'I', 'G', 'M', 'R', 'O', 'J', 'P', 'X', 'W', 'Q', 'G', 'R', 'U', 'M', 'Y', 'H', 'J', 'B', 'B', 'B', 'H', 'K', 'E', 'J', 'N', 'A', 'T', 'G', 'A', 'X', 'O', 'L', 'J', 'G', 'L', 'M', 'Y', 'K', 'J', 'V', 'M', 'Q', 'N', 'B', 'S', 'J', 'K', 'H', 'L', 'T', 'R', 'E', 'D', 'J', 'X', 'W', 'F', 'W', 'S', 'X', 'N', 'K', 'J', 'D', 'E', 'X', 'B', 'H', 'Z', 'O', 'V', 'L', 'C', 'O', 'J', 'Q', 'G', 'M', 'C', 'G', 'Y', 'V', 'S', 'G', 'I', 'N', 'Y', 'K', 'G', 'B', 'C', 'M', 'B', 'D', 'K', 'J', 'H', 'V', 'W', 'B', 'H', 'Y', 'Y', 'W', 'I', 'X', 'J', 'N', 'H', 'Z', 'B', 'R', 'J', 'Q', 'X', 'P', 'F', 'U', 'A', 'N', 'N', 'A', 'J', 'D', 'D', 'Q', 'C', 'X', 'X', 'V', 'U', 'T', 'L', 'X', 'I', 'V', 'G', 'R', 'Y', 'G', 'T', 'W', 'S', 'G', 'F', 'X', 'A', 'L', 'U', 'Y', 'I', 'K', 'N', 'H', 'K', 'F', 'A', 'T', 'N', 'Q', 'K', 'Y', 'N', 'A', 'J', 'J', 'W', 'W', 'G', 'T', 'S', 'V', 'T', 'J', 'W', 'T', 'Z', 'V', 'W', 'Y', 'B', 'X', 'N', 'U', 'W', 'S', 'W', 'K', 'D', 'S', 'L', 'N', 'I', 'G', 'X', 'B', 'K', 'Y', 'Y', 'F', 'X', 'G', 'A', 'I', 'H', 'H', 'Y', 'V', 'M', 'K', 'Z', 'B', 'H', 'L', 'W', 'S', 'N', 'E', 'D', 'V', 'U', 'W', 'U', 'F', 'G', 'O', 'W', 'R', 'Y', 'L', 'X', 'D', 'Y', 'J', 'M', 'K', 'N', 'J', 'G', 'W', 'I', 'N', 'X', 'P', 'S', 'Y', 'B', 'X', 'R', 'D', 'L', 'N', 'W', 'T', 'Q', 'D', 'F', 'F', 'F', 'R', 'X', 'L', 'K', 'G', 'S', 'T', 'Q', 'O', 'A', 'J', 'X', 'V', 'T', 'G', 'W', 'H', 'L', 'T', 'H', 'N', 'W', 'W', 'M', 'E', 'F', 'L', 'V', 'G', 'U', 'K', 'J', 'S', 'S', 'Y', 'N', 'X', 'W', 'Q', 'K', 'M', 'C', 'W', 'I', 'H', 'F', 'B', 'C', 'M', 'M', 'L', 'F', 'Y', 'B', 'X', 'R', 'H', 'K', 'X', 'U', 'Z', 'J', 'V', 'S', 'S', 'X', 'N', 'X', 'H', 'V', 'Y', 'B', 'X', 'R', 'W', 'G', 'W', 'Y', 'V', 'W', 'H', 'S', 'Y', 'Y', 'M', 'M', 'H', 'E', 'F', 'W', 'A', 'N', 'Q', 'W', 'Z', 'M', 'X', 'I', 'W', 'G', 'J', 'H', 'V', 'W', 'B', 'H', 'Y', 'N', 'A', 'J', 'P', 'L', 'M', 'I', 'L', 'J', 'F', 'G', 'I', 'Y', 'L', 'W', 'H', 'N', 'T', 'F', 'O', 'J', 'G', 'S', 'W', 'I', 'N', 'S', 'G', 'L', 'M', 'Y', 'N', 'X', 'H', 'G', 'K', 'M', 'X', 'H', 'U', 'W', 'Y', 'E', 'X', 'D', 'V', 'L', 'M', 'U', 'M', 'B', 'H', 'J', 'J', 'M', 'A', 'F', 'U', 'W', 'I', 'U', 'F', 'T', 'Q', 'Y', 'Y', 'B', 'H', 'X', 'H', 'O', 'M', 'I', 'G', 'J', 'H', 'V', 'J', 'X', 'M', 'T', 'F', 'G', 'R', 'G', 'N', 'S', 'L', 'U', 'F', 'N', 'X', 'X', 'H', 'U', 'Z', 'L', 'X', 'Q', 'B', 'L', 'M', 'Y', 'L', 'J', 'D', 'J', 'J', 'E', 'G', 'T', 'Z', 'F', 'F', 'M', 'L', 'D', 'P', 'E', 'J', 'N', 'K', 'N', 'F', 'W', 'S', 'W', 'K', 'D', 'S', 'L', 'N', 'I', 'G', 'X', 'B', 'K', 'Y', 'Y', 'F', 'X', 'D', 'F', 'I', 'B', 'T', 'A', 'H', 'S', 'B', 'Y', 'T', 'P', 'Q', 'W', 'X', 'M', 'B', 'S', 'W', 'Z', 'F', 'N', 'X', 'A', 'H', 'J', 'D', 'I', 'G', 'J', 'L', 'F', 'A', 'I', 'E', 'A', 'H', 'V', 'M', 'U', 'L', 'Y', 'R', 'H', 'T', 'M', 'L', 'J', 'V', 'K', 'Y', 'B', 'X', 'X', 'D', 'E', 'J', 'M', 'X', 'Y', 'R', 'X', 'X', 'Y', 'V', 'W', 'H', 'L', 'P', 'Y', 'R', 'X'], 'SECRET')
	encryptionmakesthemodernworldgoroundeverytimeyoumakeamobilephonecallbuysomethingwithacreditcardinashoporontheweborevengetcashfromanatmencryptionbestowsuponthattransactiontheconfidentialityandsecuritytomakeitpossibleifyouconsiderelectronictransactionsandonlinepaymentsallthosewouldnotbepossiblewithoutencryptionsaiddrmarkmanulisaseniorlecturerincryptographyattheuniversityofsurreyatitssimplestencryptionisallabouttransformingintelligiblenumbersortextsoundsandimagesintoastreamofnonsensetherearemanymanywaystoperformthattransformationsomestraightforwardandsomeverycomplexmostinvolveswappinglettersfornumbersandusemathstodothetransformationhowevernomatterwhichmethodisusedtheresultingscrambleddatastreamshouldgivenohintsabouthowitwasencryptedduringworldwariithealliesscoredsomenotablevictoriesagainstthegermansbecausetheirencryptionsystemsdidnotsufficientlyscramblemessagesrigorousmathematicalanalysisbyalliedcodecrackerslaidbarepatternshiddenwithinthemessagesandusedthemtorecreatethemachineusedtoencryptthemthosecodesrevolvedaroundtheuseofsecretkeysthatweresharedamongthosewhoneededtocommunicatesecurelytheseareknownassymmetricencryptionsystemsandhaveaweaknessinthateveryoneinvolvedhastopossessthesamesetofsecretkeys
	"""
	keyString = keyString.upper()
	keyLength = len(keyString)
	decryptedCharList = []
	subKeyIndex = 0
	for char in charList:
		subKeyLetter = keyString[subKeyIndex]
		subKey = cipher_utils.cipherLetterToOrdinal(subKeyLetter) + 1
		cipherOrdinal = cipher_utils.cipherLetterToOrdinal(char)
		plainTextOrdinal = (cipherOrdinal - subKey) % 26
		plainTextLetter = cipher_utils.ordinalToClearLetter(plainTextOrdinal)
		decryptedCharList.append(plainTextLetter)
		subKeyIndex+=1
		logger.debug('SubKey %s (%s - %s):\tcipher char: %s (%s)\tplaintext char: %s (%s)' % (subKeyIndex, subKey, subKeyLetter, char, cipherOrdinal+1, plainTextLetter, plainTextOrdinal+1))
		if subKeyIndex == keyLength:
			subKeyIndex = 0
	return ''.join(decryptedCharList)


def main():
	# When run as a main programme, work through the example at the end of the
	# PDF 'A beginner’s guide to codebreaking', supplied by the 
	# University of Southampton (A Vigenere cipher)
	print('Ensure that example.txt is present in the same directory as vigenere.py')
	input('Hit any key to continue...')
	print('Reading in file example.txt and removing all whitespace characters...')
	ciphertext = cipher_utils.stripWhitespace(cipher_utils.readFile('example.txt'))
	cipherlist=list(ciphertext)
	print('Performing standard frequency analysis on list:')
	freq = cipher_utils.frequencyAnalysis(cipherlist)
	sortedFreq = cipher_utils.sortedFrequency(freq)
	cipher_utils.displayFrequency(sortedFreq)
	input('Hit any key to continue...')
	print('Turning on debugging (DEBUG Level)...')
	setLoggingLevel(logging.DEBUG)
	print('Frequency analysis indicates a polyalphabetic cipher, so let\'s calculate the Index of Coincidence (ioc)')
	print('%s' % (cipher_utils.ioc(cipherlist)))
	input('Hit any key to continue...')
	print('Turning on debugging (INFO Level)...')
	setLoggingLevel(logging.INFO)
	print('Now calculate the ioc for all possible subkeys from 1 to 9')
	displayIocTable(cipherlist, 9)
	input('Hit any key to continue...')
	keyLength = 6
	print('Judging from the ioc table, we can guess that the keylength is %s' % (keyLength))
	print('Display frequency analysis for the %s subkeys:' % (keyLength))
	displaySubkeyFrequencies(cipherlist, keyLength)
	input('Hit any key to continue...')
	print('Most frequent letters for subkey1=X, subkey2=J, subkey3=H, subkey4=J, subkey5=Y, subkey6=Y')
	print('X=24 : 24-5=19 (S), J=10 : 10-5=5 (E), H=8 : 8-5=3 (C), J=10 : 10-5=5 (E), Y=25 : 25-5=20 (T), Y=25 : 25-5=20 (T)')
	print('Turning on debugging (DEBUG Level)...')
	setLoggingLevel(logging.DEBUG)
	print('Attempt to decipher with keyword %s' % (deriveVigenereKeyPhrase('XJHJYY')))
	input('Hit any key to continue...')
	solution = decryptVigenere(ciphertext, deriveVigenereKeyPhrase('XJHJYY'))
	print(solution)
	cipher_utils.writeFile('solution.txt', solution)
	print('This doesn\'t appear to be quite right - re-evaluate subkeys 4 & 5')
	print('Using second most frequent letters for subkeys 4 & 5: subkey1=X, subkey2=J, subkey3=H, subkey4=W, subkey5=J, subkey6=Y')
	print('X=24 : 24-5=19 (S), J=10 : 10-5=5 (E), H=8 : 8-5=3 (C), W=23 23-5=18 (R), J=10 : 10-5=5 (E), Y=25 : 25-5=20 (T)')
	print('Attempt to decipher with keyword %s' % (deriveVigenereKeyPhrase('XJHWJY')))
	print('Turning off debugging (ERROR Level)...')
	setLoggingLevel(logging.ERROR)
	input('Hit any key to continue...')
	solution = decryptVigenere(ciphertext, deriveVigenereKeyPhrase('XJHWJY'))
	print(solution)
	cipher_utils.writeFile('solution.txt', solution)

# if cipher_utils.py is run, instead of being imported as a module,
# call the main() function

# Always perform a sanity check first on the known example cipher:
print('Checking decryption logic on vigenere module...')
setLoggingLevel(logging.ERROR)
if decryptVigenere(cipher_utils.stripWhitespace('''
XSFJD JMNRF RUDJV LMYFT GWWHP TUDIA HWRMS XXAHJ DNBRH
QTOFF NWFGH GLDJJ ATQWH UEQEM DMHRH LMCGL ZAYBT HUWIC
MHDJI CGFVZ TJHWR FYBXB HTTLX AHFLY MHDKM ZKTPS SUMRH
FHLRU WATHU JVLTQ LZSGS NAFWL WUGXD UYCHS WZJWH SIAIY
GYLSQ CMDDF IMXHX JNNRY REFEX NWHTM LNEDJ CYDRM HIGXL
VJLXQ HUYLH SLUYL TSVSH NBTQK FHWTQ DNHXU DQRYG YVSQF
MMRKJ QHZOV SIMGH HTMLN EDJQB YKGZN XSFJD JMNRF XUBIG
JRUKP PSSOE NVSXY GNRJQ YVYXJ JLBSF JDJMT JJFJA DDLYB
XZQAA YKXLL DIYXX JWYRF WAYML NPHQY LYHFH LRUWA THBXD
DQUUT XLYLT SVXTL FNQYN HMJOD NABGO WSOFG HJXIK YHPYM
HZQVX UGILE FAXXL FYITX WJJUF TIFTH LJQKJ NAJUW FLXRD
FDGTS BOFSL YRHJL YTUEY BTYWJ FHLKR JRUMN RFXIF JVLWU
BLKLK IKBDJ IUGIV GRYOJ UQHIF UOWCG HXWAS PHQYW XQTUS
ASAEJ WLJLL KRJSO FGHJX UGIXK JGTYK KYIWT WZJNK FQKKI
KRDLN IGMRO JPXWQ GRUMY HJBBB HKEJN ATGAX OLJGL MYKJV
MQNBS JKHLT REDJX WFWSX NKJDE XBHZO VLCOJ QGMCG YVSGI
NYKGB CMBDK JHVWB HYYWI XJNHZ BRJQX PFUAN NAJDD QCXXV
UTLXI VGRYG TWSGF XALUY IKNHK FATNQ KYNAJ JWWGT SVTJW
TZVWY BXNUW SWKDS LNIGX BKYYF XGAIH HYVMK ZBHLW SNEDV
UWUFG OWRYL XDYJM KNJGW INXPS YBXRD LNWTQ DFFFR XLKGS
TQOAJ XVTGW HLTHN WWMEF LVGUK JSSYN XWQKM CWIHF BCMML
FYBXR HKXUZ JVSSX NXHVY BXRWG WYVWH SYYMM HEFWA NQWZM
XIWGJ HVWBH YNAJP LMILJ FGIYL WHNTF OJGSW INSGL MYNXH
GKMXH UWYEX DVLMU MBHJJ MAFUW IUFTQ YYBHX HOMIG JHVJX
MTFGR GNSLU FNXXH UZLXQ BLMYL JDJJE GTZFF MLDPE JNKNF
WSWKD SLNIG XBKYY FXDFI BTAHS BYTPQ WXMBS WZFNX AHJDI
GJLFA IEAHV MULYR HTMLJ VKYBX XDEJM XYRXX YVWHL PYRX
'''), 'SECRET') != 'encryptionmakesthemodernworldgoroundeverytimeyoumakeamobilephonecallbuysomethingwithacreditcardinashoporontheweborevengetcashfromanatmencryptionbestowsuponthattransactiontheconfidentialityandsecuritytomakeitpossibleifyouconsiderelectronictransactionsandonlinepaymentsallthosewouldnotbepossiblewithoutencryptionsaiddrmarkmanulisaseniorlecturerincryptographyattheuniversityofsurreyatitssimplestencryptionisallabouttransformingintelligiblenumbersortextsoundsandimagesintoastreamofnonsensetherearemanymanywaystoperformthattransformationsomestraightforwardandsomeverycomplexmostinvolveswappinglettersfornumbersandusemathstodothetransformationhowevernomatterwhichmethodisusedtheresultingscrambleddatastreamshouldgivenohintsabouthowitwasencryptedduringworldwariithealliesscoredsomenotablevictoriesagainstthegermansbecausetheirencryptionsystemsdidnotsufficientlyscramblemessagesrigorousmathematicalanalysisbyalliedcodecrackerslaidbarepatternshiddenwithinthemessagesandusedthemtorecreatethemachineusedtoencryptthemthosecodesrevolvedaroundtheuseofsecretkeysthatweresharedamongthosewhoneededtocommunicatesecurelytheseareknownassymmetricencryptionsystemsandhaveaweaknessinthateveryoneinvolvedhastopossessthesamesetofsecretkeys':
	print('Error testing decryptVigenere(charList, keyString) method!!! Check your code before continuing...')
	sys.exit()
elif deriveVigenereKeyPhrase('XJHWJY') != 'SECRET':
	print('Error testing deriveVigenereKeyPhrase(frequentChars) method!!! Check your code before continuing...')
	sys.exit()
else:
	print('decryption logic OK.')

if __name__ == '__main__':
	main()
