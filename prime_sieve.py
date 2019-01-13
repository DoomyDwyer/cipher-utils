# Prime Number Sieve
# Author: Al Sweigart (Hacking Secret Ciphers with Python)
# http://inventwithpython.com/hacking (BSD Licensed)

import math

def primeSieve(sieveSize):
	# Returns a list of prime numbers calculated using
	# the Sieve of Erastothenes algorithm.
	
	sieve = [True] * sieveSize
	sieve[0] = False # zero and one are not prime numbers
	sieve[1] = False
	
	# create the sieve
	sqrtSieveSize = int(math.sqrt(sieveSize)) + 1
	for i in range(2, sqrtSieveSize):
		pointer = i * 2
		while pointer < sieveSize:
			sieve[pointer] = False
			pointer += i
	return sieve

def listPrimes(sieveSize):
	# Retrieve the sieve using Erastothenes' algorithm:
	sieve = primeSieve(sieveSize)
	
	# Compile the list of primes
	primes = []
	for i in range(sieveSize):
		if sieve[i]:
			primes.append(i)
	return primes
