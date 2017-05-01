# bifid.py
# Author: Steve Dwyer

import sys, logger, cipher_utils

def displayKeySquare(keyString):
	n = 0
	keySquare = ['\n', ' ', ' ']
	for y in range(5):
		keySquare.append(' ' + str(y))
	keySquare.append('\n')
	for x in range(5):
		keySquare.append(' ' + str(x))
		for y in range(5):
			keySquare.append(' ' + keyString[n])
			n += 1
		keySquare.append('\n')
	return ''.join(keySquare)

def checkKey(keyString):
	if len(keyString) != 25:
		logger.error('Key Square is not 5x5!')
		return False
	for char in keyString:
		if char == 'J':
			logger.error('Key Square contains a J!')
			return False
		if not char.isalpha():
			logger.error('Key Square contains non-alphabetic characters!')
			return False
	logger.debug(displayKeySquare(keyString))
	return True

def formatKeyString(keyString):
	keyString = keyString.upper()
	return keyString

def formatMessage(charList):
	charList = charList.upper()
	charList.replace('J', 'I')
	return charList

def getCoordsFromKeySquareChars(charList, keyString):
	coords = []
	for char in charList:
		absCoord = keyString.find(char)
		xCoord = absCoord // 5
		yCoord = absCoord % 5
		charCoords = [xCoord, yCoord]
		logger.debug('%s = %s' % (char, charCoords))
		coords.append(charCoords)
	logger.debug('coords = %s' % (coords))
	return coords

def getCharsFromKeySquareCoords(fractionatedCoords, keyString):
	charList = []
	for charCoords in fractionatedCoords:
		charIndex = charCoords[0] * 5 + charCoords[1]
		char = keyString[charIndex]
		logger.debug('%s = %s' % (char, charCoords))
		charList.append(char)
	logger.debug('charList = %s' % (charList))
	return ''.join(charList)

def defractionate(coords, period):
	defractionatedCoords = []
	periodElementNr = 0
	fractionatedBlock = []
	for n in range(len(coords)):
		fractionatedBlock.append(coords[n][0])
		fractionatedBlock.append(coords[n][1])
		periodElementNr += 1
		if periodElementNr == period or n == len(coords) -1:
			# period is full, or end of text reached: defractionate
			logger.debug('fractionatedBlock = %s' % (fractionatedBlock))
			periodCoords = []
			for elementNr in range(periodElementNr):
				charCoords = [fractionatedBlock[elementNr], fractionatedBlock[elementNr + periodElementNr]]
				periodCoords.append(charCoords)
				defractionatedCoords.append(charCoords)
			logger.debug('defractionated period coords = %s' % (periodCoords))
			periodElementNr = 0
			fractionatedBlock = []
	return defractionatedCoords

def fractionate(coords, period):
	fractionatedCoords = []
	periodElementNr = 0
	periodCoordsLeft = []
	periodCoordsRight = []
	for n in range(len(coords)):
		periodCoordsLeft.append(coords[n][0])
		periodCoordsRight.append(coords[n][1])
		periodElementNr += 1
		if periodElementNr == period or n == len(coords) -1:
			# period is full, or end of text reached: fractionate
			logger.debug('periodCoords = %s %s' % (periodCoordsLeft, periodCoordsRight))
			fractionatedBlock = periodCoordsLeft + periodCoordsRight
			logger.debug('fractionated block = %s' % (fractionatedBlock))
			fractionatedPeriodCoords = []
			for elementNr in range(0, len(fractionatedBlock), 2):
				charCoords = [fractionatedBlock[elementNr], fractionatedBlock[elementNr +1]]
				fractionatedPeriodCoords.append(charCoords)
				fractionatedCoords.append(charCoords)
			logger.debug('fractionated period coords = %s' % (fractionatedPeriodCoords))
			periodElementNr = 0
			periodCoordsLeft = []
			periodCoordsRight = []
	return fractionatedCoords

def bifid(charList, keyString, period, operation):
	keyString = formatKeyString(keyString)
	if not checkKey(keyString):
		return None
	charList = formatMessage(charList)
	coords = getCoordsFromKeySquareChars(charList, keyString)
	fractionatedCoords = operation(coords, period)
	ciphertext = getCharsFromKeySquareCoords(fractionatedCoords, keyString)
	return ciphertext

def encryptBifid(charList, keyString, period):
	""" (list, str, int) -> str
	
	Encrypt the passed plaintext list charList with the Bifid cipher
	using the passed key keyString and period period.
	
	>>> encryptBifid('defendtheeastwallofthecastle', 'phqgmeaylnofdxkrcvszwbuti', 5)
	FFYHMKHYCPLIASHADTRLHCCHLBLR
	"""
	ciphertext = bifid(charList, keyString, period, fractionate).upper()
	logger.info('%s' % (ciphertext))
	return ciphertext

def decryptBifid(charList, keyString, period):
	""" (list, str, int) -> str
	
	Decrypt the passed ciphertext list charList, encrypted with the Bifid cipher
	using the passed key keyString and period period.
	
	>>> decryptBifid('FFYHMKHYCPLIASHADTRLHCCHLBLR', 'phqgmeaylnofdxkrcvszwbuti', 5)
	defendtheeastwallofthecastle
	"""
	plaintext = bifid(charList, keyString, period, defractionate).lower()
	logger.info('%s' % (plaintext))
	return plaintext

def main():
	import cipher_utils
	print('Ensure that plaintext.txt is present in the same directory as bifid.py')
	input('Hit any key to continue...')
	print('Reading in file plaintext.txt and removing all whitespace characters...')
	plaintext = cipher_utils.stripWhitespace(cipher_utils.readFile('plaintext.txt'))
	logger.setLevel(logger.ERROR)
	print(plaintext)
	print('Ready to encrypt')
	input('Hit any key to continue...')
	logger.setLevel(logger.ERROR)
	ciphertext = encryptBifid(plaintext, 'LIGOABCDEFHKMNPQRSTUVWXYZ', 4)
	print(ciphertext)
	cipher_utils.writeFile('solution.txt', ciphertext)
	logger.setLevel(logger.ERROR)
	print('Ensure that cipher.txt is present in the same directory as bifid.py')
	input('Hit any key to continue...')
	print('Reading in file cipher.txt and removing all whitespace characters...')
	ciphertext = cipher_utils.stripWhitespace(cipher_utils.readFile('cipher.txt'))
	logger.setLevel(logger.ERROR)
	print(ciphertext)
	print('Ready to decrypt')
	input('Hit any key to continue...')
	logger.setLevel(logger.ERROR)
	plaintext = decryptBifid(ciphertext, 'LIGOABCDEFHKMNPQRSTUVWXYZ', 4)
	print(plaintext)
	cipher_utils.writeFile('solution.txt', plaintext)
	logger.setLevel(logger.ERROR)

# Always perform a sanity check first on the known example cipher:
print('Checking encryption logic on bifid module...')
logger.setLevel(logger.ERROR)
if encryptBifid('defen', 'phqgmeaylnofdxkrcvszwbuti', 5) != 'FFYHM':
	print('Error testing encryptBifid(charList, keyString, period) method!!! Check your code before continuing...')
	sys.exit()
if encryptBifid('defendtheeastwallofthecastle', 'phqgmeaylnofdxkrcvszwbuti', 5) != 'FFYHMKHYCPLIASHADTRLHCCHLBLR':
	print('Error testing encryptBifid(charList, keyString, period) method!!! Check your code before continuing...')
	sys.exit()
print('encryption logic OK.')
print('Checking decryption logic on bifid module...')
logger.setLevel(logger.ERROR)
if decryptBifid('FFYHM', 'phqgmeaylnofdxkrcvszwbuti', 5) != 'defen':
	print('Error testing decryptBifid(charList, keyString, period) method!!! Check your code before continuing...')
	sys.exit()
if decryptBifid('FFYHMKHYCPLIASHADTRLHCCHLBLR', 'phqgmeaylnofdxkrcvszwbuti', 5) != 'defendtheeastwallofthecastle':
	print('Error testing decryptBifid(charList, keyString, period) method!!! Check your code before continuing...')
	sys.exit()
print('decryption logic OK.')
logger.setLevel(logger.ERROR)

# if bifid.py is run, instead of being imported as a module,
# call the main() function

if __name__ == '__main__':
	main()
