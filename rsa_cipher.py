# RSA Cipher
# Author: Al Sweigart (Hacking Secret Ciphers with Python)
# http://inventwithpython.com/hacking (BSD Licensed)

import sys

# IMPORTANT: The block size MUST be less than or equal to the key size!
# (Note: the block size is in bytes, the keysize is in bits.
# There are 8 bits in 1 byte.)
DEFAULT_BLOCK_SIZE = 128 # 128 bytes
BYTE_SIZE = 256 # One byte has 256 different values

def main(mode = 'encrypt'):
	''' (str) -> None
	
	Runs a test that encrypts a message to a file or decrypts a message from a file.
	
	Parameter mode determines whether to encrypt or decrypt:
	
	mode = 'encrypt' (default): Message defined in the main function will be encrypted using Alice's PUBLIC key and written to file 'encrypted_file.txt'
	mode = 'decrypt': File 'encrypted_file.txt' will be read and decrypted using Alice's PRIVATE key.
	'''
	filename = 'encrypted_file.txt'
	
	if mode == 'encrypt':
		plainText = '''"Journalists belong in the gutter because that is where the ruling classes throw their guilty secrets." -Gerald Priestland "The Founding Fathers gave the free press the protection it must have to bare the secrets of government and inform the people" -Hugo Black'''
		
		pubKeyFilename = 'alice_pubkey.txt'
		print('Encrypting and writing to %s...' % (filename))
		# Encrypt the message
		cipherText = encrypt(pubKeyFilename, plainText)

		# Save to a file
		writeToFile(filename, cipherText)
		
		print('Encrypted text:')
		print(cipherText)
		
	elif mode == 'decrypt':
		
		privKeyFilename = 'alice_privkey.txt'
		print('Reading from %s and decrypting...' % (filename))
		# Read from a file
		encryptedText = readFromFile(filename)

		# Decrypt the message
		decryptedText = decrypt(privKeyFilename, encryptedText)
		
		print('Decrypted text:')
		print(decryptedText)
		
def getBlocksFromText(message, blockSize = DEFAULT_BLOCK_SIZE):
	# Converts a string message to a list of block integers. Each integers
	# represents 128 (or whatever the blockSize is set to) string characters
	
	messageBytes = message.encode('ascii') # convert the string to bytes
	
	blockInts = []
	for blockStart in range(0, len(messageBytes), blockSize):
		# Calculate the block integer for this block of text
		blockInt = 0
		for i in range(blockStart, min(blockStart + blockSize, len(messageBytes))):
			blockInt += messageBytes[i] * (BYTE_SIZE ** (i % blockSize))
		blockInts.append(blockInt)
	return blockInts
	
def getTextFromBlocks(blockInts, messageLength, blockSize = DEFAULT_BLOCK_SIZE):
	# Converts a list of block integers to the original message string.
	# The original message length is needed to properly convert the last block integer.
	message = []
	for blockInt in blockInts:
		blockMessage = []
		for i in range(blockSize - 1, -1, -1):
			if len(message) + 1 < messageLength:
				# Decode the message string for the 128 (or whatever blockSize is set to) characters
				# from this block integer
				asciiNumber = blockInt // (BYTE_SIZE ** i)
				blockInt = blockInt % (BYTE_SIZE ** i)
				blockMessage.insert(0, chr(asciiNumber))
		message.extend(blockMessage)
	return ''.join(message)
	
def encryptMessage(message, key, blockSize = DEFAULT_BLOCK_SIZE):
	# Converts the message String into a list of block integers, and then
	# encrypts each block integer. Pass the intended recipient's PUBLIC key to encrypt.
	# Returns the encrypted message as a string.
	encryptedBlocks = []
	n, e = key
	
	for block in getBlocksFromText(message, blockSize):
		# cipertext = plaintext ^ e mod n
		encryptedBlocks.append(pow(block, e, n))
	
	# Convert the large int values to one string value
	for i in range(len(encryptedBlocks)):
		encryptedBlocks[i] = str(encryptedBlocks[i])
	
	encryptedContent = ','.join(encryptedBlocks)
	return encryptedContent
	
def decryptMessage(encryptedMessage, messageLength, key, blockSize = DEFAULT_BLOCK_SIZE):
	# Decrypts an encrypted message into the original message string.
	# The original message length is required to properly decrypt the last block.
	# Be sure to pass the recipent's PRIVATE key to decrypt.
	
	# Convert the encrypted message into large int values
	encryptedBlocks = []
	for block in encryptedMessage.split(','):
		encryptedBlocks.append(int(block))
	
	decryptedBlocks = []
	n, d = key
	for block in encryptedBlocks:
		# plaintext = ciphertext ^ d mon n
		decryptedBlocks.append(pow(block, d, n))
	return getTextFromBlocks(decryptedBlocks, messageLength, blockSize)
	
def encrypt(keyFilename, message, blockSize = DEFAULT_BLOCK_SIZE):
	''' (str, str, int) -> str
	
	Using a key from a key file, encrypt the plain text message.
	Pass the intended recipient's PUBLIC key to encrypt, or your PRIVATE key to sign.
	Returns the encrypted message string
	'''
	keySize, n, e = readKeyFile(keyFilename)
	
	# Check that key size is greater than block size
	if keySize < blockSize * 8: # * 8 to convert bytes to bits
		sys.exit('ERROR: Block size is %s bits and key size is %s bits. The RSA cipher requires the block size to be equal to or greater than the key size. Either decrease the block size or use different keys.' % (blockSize * 8, keySize))
	
	# Encrypt the message
	encryptedContent = encryptMessage(message, (n, e), blockSize)
	encryptedContent = '%s_%s_%s' % (len(message), blockSize, encryptedContent)
	return encryptedContent

def decrypt(keyFilename, content):
	''' (str, str) -> str
	
	Using a key from a key file, decrypt an encrypted message.
	Pass your PRIVATE key to decrypt, or the sender's PUBLIC key to verify signature.
	Returns the decrypted message string.
	'''
	keySize, n, d = readKeyFile(keyFilename)
	
	messageLength, blockSize, encryptedMessage = content.split('_')
	messageLength = int(messageLength)
	blockSize = int(blockSize)
	
	# Check that key size is greater than block size
	if keySize < blockSize * 8: # * 8 to convert bytes to bits
		sys.exit('ERROR: Block size is %s bits and key size is %s bits. The RSA cipher requires the block size to be equal to or greater than the key size. Did you specific the correct key file and encrypted file?' % (blockSize * 8, keySize))
	
	# Decrypt the large int values
	return decryptMessage(encryptedMessage, messageLength, (n, d), blockSize)
	
def readKeyFile(keyFilename):
	# Given the filename of a file that contains a public or private key,
	# return the key as a (n,e) or (n,d) tuple value
	fo = open(keyFilename)
	content = fo.read()
	fo.close()
	keySize, n, EorD = content.split(',')
	return (int(keySize), int(n), int(EorD))
	
def writeToFile(filename, content):
	''' (str, str) -> None
	
	Write out the passed contents to a text file
	'''
	fo = open(filename, 'w')
	fo.write(content)
	fo.close()
	
def readFromFile(filename):
	''' (str) -> str
	
	Read in the contents from a text file.
	Returns the contents.
	'''
	fo = open(filename)
	content = fo.read()
	fo.close()
	return content
	
# If rsa_cipher.py is run (instead of imported as a module), call the main() function
if __name__ == '__main__':
	main()
