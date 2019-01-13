# Primality Testing with the Rabin-Miller Algorithm
# Author: Al Sweigart (Hacking Secret Ciphers with Python)
# http://inventwithpython.com/hacking (BSD Licensed)
# Adapted by Steve Dwyer to correspond more closely to the pseudocode example set out at:
# https://en.wikipedia.org/wiki/Miller–Rabin_primality_test#Example

import random

def rabinMiller(n, k=5):
	# Returns True if n is probably prime
	probablyPrime = True
	
	# determine n − 1 as 2**r * d with d odd by factoring powers of 2 from n − 1
	d = n - 1
	r = 0
	while d % 2 == 0: 
		# Keep halving d until it is odd
		# (and use r to count how many times we halve d)
		d = d // 2
		r += 1
		#print('d=%s, r=%d' % (d, r))
	
	for witnesses in range(k): # try to falsify n's primality k times
		a = random.randrange(2, n - 1)
		x = pow(a, d, n)
		#print('a=%s, d=%s, x=%d, n=%s' % (a, d, x, n))

		if x == 1 or x == n - 1: # this test does not apply if x is 1 or n -1
			continue
		for i in range (r - 1):
			x = pow(x, 2, n)
			#print('i=%s, x=%d, n=%s' % (i, x, n))
			if x == n - 1:
				break

		if x == n - 1:
			continue
		else:
			probablyPrime = False
			break
	return probablyPrime

def isPrime(n):
	# Return True is n is a prime number. This function does a quicker
	# prime number check before calling rabinMiller().
	
	if (n < 2):
		return False # 0, 1 and negative numbers are not prime
	
	# About 1/3 of the  time we can quickly determine whether n is not prime
	# by dividing by the first few dozen prime numbers. This is quicker than rabinMiller(),
	# but unlike rabinMiller() is not guaranteed to prove that a number is not a prime.
	lowPrimes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317, 331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433, 439, 443, 449, 457, 461, 463, 467, 479, 487, 491, 499, 503, 509, 521, 523, 541, 547, 557, 563, 569, 571, 577, 587, 593, 599, 601, 607, 613, 617, 619, 631, 641, 643, 647, 653, 659, 661, 673, 677, 683, 691, 701, 709, 719, 727, 733, 739, 743, 751, 757, 761, 769, 773, 787, 797, 809, 811, 821, 823, 827, 829, 839, 853, 857, 859, 863, 877, 881, 883, 887, 907, 911, 919, 929, 937, 941, 947, 953, 967, 971, 977, 983, 991, 997]

	if n in lowPrimes:
		return True
	
	# See if any of the low primes can divide n
	for prime in lowPrimes:
		if n % prime == 0:
			return False
	
	# If all else fails, call rabinMiller() to determine if n is a prime
	return rabinMiller(n)

def generateLargePrime(keysize=1024):
	# Return a random prime number of keysize bits is size.
	while True:
		n = random.randrange(2**(keysize-1), 2**keysize)
		if isPrime(n):
			return n
