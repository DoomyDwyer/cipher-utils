# hill.py
# Author: Steve Dwyer

import sys, logging, logger, cipher_utils

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
	# Only proven to work on a 2x2 matrix (4 letter keyword) for now
	# First, find the determinant det K of keyMatrix K
	det = 0
	m = n = p = len(keyMatrix)
	for i in range (m // 2):
		for j in range (n):
			subDet = cipher_utils.cipherLetterToOrdinal(keyMatrix[i][j]) * cipher_utils.cipherLetterToOrdinal(keyMatrix[m-1][n-1])
			if i == j:
				det += subDet
			else:
				det -= subDet
			logger.debug('determinant=%s, i=%s, j=%s, m=%s, n=%s, keyL=%s, keyR=%s' % (det, i, j, m, n, cipher_utils.cipherLetterToOrdinal(keyMatrix[i][j]), cipher_utils.cipherLetterToOrdinal(keyMatrix[m-1][n-1])))
			n-=1
		n=p
		m-=1
	det = det % 26
	logger.debug('determinant = %s' % (det))

	# Next, find the multiplicative inverse of the determinant det K
	di=0;
	for x in range(26):
		if (det * x) % 26 == 1:
			di = x
	if di == 0:
		print('could not invert, try different key')
		return None
	logger.debug('multiplicative inverse K**-1 of the determinant det K (such that (det * x) mod 26 = 1 : %s' % (di))
	keyInverseMatrix = []
	m = n = p = len(keyMatrix)
	for i in range (p):
		row = []
		for j in range (p):
			if i == j:
				inverse = di * cipher_utils.cipherLetterToOrdinal(keyMatrix[m-1][n-1])
				logger.debug('m=%s, n=%s row[%s][%s] = %s (mod 26)' % (m-1, n-1, i, j, inverse))
			else:
				inverse = -1 * di * cipher_utils.cipherLetterToOrdinal(keyMatrix[i][j])
				logger.debug('i=%s, j=%s row[%s][%s] = %s (mod 26)' % (i, j, i, j, inverse))
			inverse = inverse % 26
			row.append(inverse)
			logger.debug('row[%s][%s] = %s' % (i, j, inverse))
			n-=1
		keyInverseMatrix.append(row)
		n=p
		m-=1
	logger.debug('keyInverseMatrix = %s' % (keyInverseMatrix))
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
	logger.debug('%sing %s' % (mode, charList))
	keyMatrix = getKeyMatrix(keyString)
	textLength = len(charList)
	keyLength = len(keyString)
	n = keyLength // 2
	cipherlist = []
	charNr = 0
	while charNr < textLength:
		colVector = []
		logger.debug('charNr=%s' % (charNr))
		logger.debug('charNr=%s, charList[charNr]=%s' % (charNr, charList[charNr]))
		for i in range(n):
			logger.debug('i=%s, n=%s' % (i, n))
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
	import cipher_utils
	print('Ensure that plaintext.txt is present in the same directory as hill.py')
	input('Hit any key to continue...')
	print('Reading in file plaintext.txt and removing all whitespace characters...')
	plaintext = cipher_utils.stripWhitespace(cipher_utils.readFile('plaintext.txt'))
	logger.setLoggingLevel(logging.ERROR)
	logger.debug('%s' % (plaintext))
	plaintextlist = list(plaintext)
	print(plaintext)
	print('Ready to encrypt')
	input('Hit any key to continue...')
	logger.setLoggingLevel(logging.ERROR)
	ciphertext = hillCipher(plaintextlist, 'HILL')
	print(ciphertext)
	cipher_utils.writeFile('solution.txt', ciphertext)
	logger.setLoggingLevel(logging.ERROR)
	print('Ensure that cipher.txt is present in the same directory as hill.py')
	input('Hit any key to continue...')
	print('Reading in file cipher.txt and removing all whitespace characters...')
	ciphertext = cipher_utils.stripWhitespace(cipher_utils.readFile('cipher.txt'))
	logger.setLoggingLevel(logging.ERROR)
	logger.debug('%s' % (ciphertext))
	cipherlist = list(ciphertext)
	print(ciphertext)
	print('Ready to decrypt')
	input('Hit any key to continue...')
	logger.setLoggingLevel(logging.ERROR)
	plaintext = hillCipher(cipherlist, 'HILL', mode='decrypt')
	print(plaintext)
	cipher_utils.writeFile('solution.txt', plaintext)
	logger.setLoggingLevel(logging.ERROR)

# if hill.py is run, instead of being imported as a module,
# call the main() function

# Always perform a sanity check first on the known example cipher:
print('Checking encryption logic on hill module...')
logger.setLoggingLevel(logging.ERROR)
if hillCipher(['A', 'B', 'C', 'D'], 'HILL') != 'ILMD':
	print('Error testing hillCipher(charList, keyString) method!!! Check your code before continuing...')
	sys.exit()
else:
	print('encryption logic OK.')
print('Checking decryption logic on hill module...')
logger.setLoggingLevel(logging.ERROR)
if hillCipher(['I', 'L', 'M', 'D'], 'HILL', mode='decrypt') != 'ABCD':
	print('Error testing hillCipher(charList, keyString, mode=\'decrypt\') method!!! Check your code before continuing...')
	sys.exit()
else:
	print('decryption logic OK.')
logger.setLoggingLevel(logging.ERROR)

if __name__ == '__main__':
	main()
