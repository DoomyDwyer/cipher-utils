# simple_sub.py
# Author: Steve Dwyer

import sys, logger, cipher_utils

def decryptSimpleSubstitutionCipher(charList, keyString, dummy=None):
	""" (list, str, str) -> str
	
	Decrypt the passed ciphertext list charList, encrypted with simple substitution cipher
	using the passed key keyString. Dummy characters are defined by the argument dummy,
	which, if set, will simply display the ciphertext character
	
	>>> decryptSimpleSubstitutionCipher(['A', 'B', 'C', ' ', 'Z'], 'KEYABCDFGHIJLMNOPQRSTUVWX.', dummy='.')
	'key Z'
	"""
	decryptedCharList = []
	logger.debug('Cipher\tPlain')
	for char in charList:
		cipherOrdinal = cipher_utils.cipherLetterToOrdinal(char)
		if cipherOrdinal in range(len(keyString)):
			plainTextLetter = keyString[cipherOrdinal].lower()
			if plainTextLetter == dummy:
				plainTextLetter = char
		else:
			plainTextLetter = char
		decryptedCharList.append(plainTextLetter)
		logger.debug('%s\t%s' % (char, plainTextLetter))
	return ''.join(decryptedCharList)

# Always perform a sanity check first on the known example cipher:
print('Checking decryption logic on simple_sub module...')
logger.setLevel(logger.ERROR)
if decryptSimpleSubstitutionCipher(['A', 'B', 'C', ' ', 'Z'], 'KEYABCDFGHIJLMNOPQRSTUVWX.') != 'key .':
	print('Error testing decryptSimpleSubstitutionCipher(charList, keyString) method!!! Check your code before continuing...')
	sys.exit()
elif decryptSimpleSubstitutionCipher(['A', 'B', 'C', ' ', 'Z'], 'KEYABCDFGHIJLMNOPQRSTUVWX.', dummy='.') != 'key Z':
	print('Error testing decryptSimpleSubstitutionCipher(charList, keyString) method!!! Check your code before continuing...')
	sys.exit()
else:
	print('decryption logic OK.')
logger.setLevel(logger.ERROR)

# if simple_sub.py is run, instead of being imported as a module,
# call the main() function

if __name__ == '__main__':
	main()
