# RSA Key generator
# Author: Al Sweigart (Hacking Secret Ciphers with Python)
# http://inventwithpython.com/hacking (BSD Licensed)

import random, sys, os, rabin_miller, cryptomath

def main():
	# Create a public/private keypair for Bob & Alice with 1024 bit keys
	print('Making key files...')
	makeKeyFiles('bob', 1024)
	makeKeyFiles('alice', 1024)
	print('Key files made.')

def generateKey(keySize):
	# Generates a public/private keypair with keys that are keySize bits in size.
	# This function may take a while to run.
	
	# Step 1: Create two prime numbers, p and q. Calculate n = p * q.
	print('Generating p prime...')
	p = rabin_miller.generateLargePrime(keySize)
	print('Generating q prime...')
	q = rabin_miller.generateLargePrime(keySize)
	n = p * q
	
	# Step 2: Create a number e that is relatively prime to (p-1)*(q-1).
	print('Generate e that is relatively prime to (p-1)*(q-1)...')
	phiPq = (p - 1) * (q - 1)
	while True:
		# Keep trying random numbers for e until one is valid
		e = random.randrange(2**(keySize-1), 2**keySize)
		if cryptomath.gcd(e, phiPq) == 1:
			break
	
	# Step 3: Calculate d, the mod inverse of e.
	print('Calculating d that is the mod inverse of e...')
	d = cryptomath.findModInverse(e, phiPq)
	
	publicKey = (n, e)
	privateKey = (n, d)
	
	print('Public Key:', publicKey)
	print('Private Key:', privateKey)
	
	return (publicKey, privateKey)
	
def makeKeyFiles(name, keySize):
	# Creates two files, '<name>_pubkey.txt' and '<name>_privkey.txt' with the n,e and n,d integers
	# written in them, delimited by a comma.
	
	# Our safety check will prevent us from overwriting our old key files:
	if os.path.exists('%s_pubkey.txt' % (name)) or os.path.exists('%s_privkey.txt' % (name)):
		sys.exit('WARNING: The file %s_pubkey.txt or %s_privkey.txt already exists! Use a different name or delete these files and re-run this program.' % (name, name))
	
	publicKey, privateKey = generateKey(keySize)
	
	print()
	print('The public key is a %s and %s digit number.' % (len(str(publicKey[0])), len(str(publicKey[1]))))
	print('Writing public key to file %s_pubkey.txt...' % (name))
	fo = open('%s_pubkey.txt' % (name), 'w')
	fo.write('%s,%s,%s' % (keySize, publicKey[0], publicKey[1]))
	fo.close()
	
	print()
	print('The private key is a %s and %s digit number.' % (len(str(privateKey[0])), len(str(privateKey[1]))))
	print('Writing private key to file %s_privkey.txt...' % (name))
	fo = open('%s_privkey.txt' % (name), 'w')
	fo.write('%s,%s,%s' % (keySize, privateKey[0], privateKey[1]))
	fo.close()

# If make_rsa_keys.py is run (instead of being imported as a module) call the main() function
if __name__ == '__main__':
	main()
