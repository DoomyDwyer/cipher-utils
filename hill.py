# hill.py
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

def getKeyMatrix(keyString):
	keyLength = len(keyString)
	m = n = keyLength // 2
	logger.debug('Matrix Dimensions = %sx%s' % (m ,n))
	matrix = []
	charNr = 0
	while charNr < keyLength:
		for i in range(m):
			row = []
			for j in range(n):
				row.append(keyString[charNr])
				charNr+=1
			logger.debug('row = %s' % (row))
			matrix.append(row)
	logger.debug('key matrix = %s' % (matrix))
	return matrix

def getMatrixInverse(keyMatrix):
	# calc inv matrix
	det = 0
	m = n = p = len(keyMatrix)
#	for i in range (m // 2)
#		for j in range (n // 2)
#			det += keyMatrix[0]*keyMatrix[3] - keyMatrix[1]*keyMatrix[2];
	for i in range (m):
		for j in range (n):
			subDet = cipher_utils.cipherLetterToOrdinal(keyMatrix[i][j]) * cipher_utils.cipherLetterToOrdinal(keyMatrix[m-1][n-1])
			if i == j:
				det -= subDet
			else:
				det += subDet
			logger.debug('det=%s, i=%s, j=%s, m=%s, n=%s, keyL=%s, keyR=%s' % (det, i, j, m, n, cipher_utils.cipherLetterToOrdinal(keyMatrix[i][j]), cipher_utils.cipherLetterToOrdinal(keyMatrix[m-1][n-1])))
			n-=1
		n=p
		m-=1
	det = ((det % 26) + 26 )% 26
	logger.debug('det=%s' % (det))
	di=0;
	for i in range(26):
		if (det * i) % 26 == 1:
			di = i
	if di == 0:
		print('could not invert, try different key')
		return None
	keyInverseMatrix = []
	m = n = p = len(keyMatrix)
	for i in range (m):
		row = []
		for j in range (n):
			inverse = di * cipher_utils.cipherLetterToOrdinal(keyMatrix[m-1][n-1])
			if i == j:
				inverse *= -1
			inverse = inverse % 26
			row.append(inverse)
			logger.debug('keyInverseMatrix[%s][%s] = %s' % (i, j, inverse))
			n-=1
		keyInverseMatrix.append(row)
		n=p
		m-=1
#	keyInverseMatrix[1] = (-1*di*keys[1])%26
#	keyInverseMatrix[2] = (-1*di*keys[2])%26
#	keyInverseMatrix[3] = di*keys[0]
#	for(i= in range(4):
#		if keyInverseMatrix[i] < 0:
#			keyInverseMatrix[i] += 26
	return keyInverseMatrix

def matrixInverseMult(keyMatrix, colVector):
	m = n = len(keyMatrix)
	keyInverseMatrix = getMatrixInverse(keyMatrix)
	letterBlock = []
	for i in range(n):
		productElement = 0
		for j in range(m):
			inverseKeyOrd = keyInverseMatrix[i][j]
			letter = colVector[j]
			letterOrd = cipher_utils.cipherLetterToOrdinal(letter)
			productElement += inverseKeyOrd * letterOrd
		cipherOrd = (productElement) % 26
		cipherLetter = cipher_utils.integerToChr(cipherOrd)
		logger.debug('%s x  %s (%s) = %s (%s)' % (inverseKeyOrd, letter, letterOrd, cipherOrd, cipherLetter))
		letterBlock.append(cipherLetter)
	return ''.join(letterBlock)

def matrixMult(keyMatrix, colVector):
	m = n = len(keyMatrix)
	letterBlock = []
	for i in range(n):
		productElement = 0
		for j in range(m):
			keyLetter = keyMatrix[i][j]
			keyOrd = cipher_utils.cipherLetterToOrdinal(keyLetter)
			letter = colVector[j]
			letterOrd = cipher_utils.cipherLetterToOrdinal(letter)
			productElement += keyOrd * letterOrd
		cipherOrd = (productElement) % 26
		cipherLetter = cipher_utils.integerToChr(cipherOrd)
		logger.debug('%s (%s) x  %s (%s) = %s (%s)' % (keyLetter, keyOrd, letter, letterOrd, cipherOrd, cipherLetter))
		letterBlock.append(cipherLetter)
	return ''.join(letterBlock)

def hillCipher(charList, keyString, mode='encrypt'):
	keyMatrix = getKeyMatrix(keyString)
	keyLength = len(keyString)
	n = keyLength // 2
	cipherlist = []
	charNr = 0
	while charNr < keyLength:
		colVector = []
		for i in range(n):
			colVector.append(charList[charNr])
			charNr+=1
		if mode == 'encrypt':
			letterBlock = matrixMult(keyMatrix, colVector)
		else:
			letterBlock = matrixInverseMult(keyMatrix, colVector)
		logger.debug('letter block = %s' % (letterBlock))
		cipherlist.append(letterBlock)
	logger.debug('cipherlist = %s' % (cipherlist))
	ciphertext = ''.join(cipherlist)
	logger.debug('ciphertext = %s' % (ciphertext))
	return ciphertext

def main():
	print('Ensure that cipher.txt is present in the same directory as scratch.py')
	input('Hit any key to continue...')
	print('Reading in file cipher.txt and removing all whitespace characters...')
	import cipher_utils
	ciphertext = cipher_utils.stripWhitespace(cipher_utils.readFile('cipher.txt'))
	setLoggingLevel(logging.ERROR)
	logger.debug('%s' % (ciphertext))
	cipherlist = cipherbintext.split()
	print(cipherlist)
	print('Ready to decrypt')
	input('Hit any key to continue...')
	plaintext = cipher_utils.hillCipher(cipherlist, 'HILL', mode='decrypt')
	print(plaintext)
	cipher_utils.writeFile('solution.txt', plaintext)
	setLoggingLevel(logging.ERROR)

# if hill.py is run, instead of being imported as a module,
# call the main() function

# Always perform a sanity check first on the known example cipher:
print('Checking encryption logic on hill module...')
setLoggingLevel(logging.DEBUG)
if hillCipher(['A', 'B', 'C', 'D'], 'HILL') != 'ILMD':
	print('Error testing hillCipher(charList, keyString) method!!! Check your code before continuing...')
	sys.exit()
else:
	print('encryption logic OK.')
print('Checking decryption logic on hill module...')
if hillCipher(['I', 'L', 'M', 'D'], 'HILL', mode='decrypt') != 'ABCD':
	print('Error testing hillCipher(charList, keyString, mode=\'decrypt\') method!!! Check your code before continuing...')
	sys.exit()
else:
	print('decryption logic OK.')

if __name__ == '__main__':
	main()
