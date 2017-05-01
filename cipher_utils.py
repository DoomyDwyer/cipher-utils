# cipher_utils.py
# Author: Steve Dwyer
# (with the exception of those functions attributed to other authors)

import sys, logger

def readFile(fileName):
	file = open(fileName)
	contents = file.read()
	file.close()
	return contents

def writeFile(fileName, contents):
	file = open(fileName, "w")
	file.write(contents)
	file.close()

def gcd(a, b):
	# Return the GCD of a and b using Euclid's algorithm
	# Author: Al Sweigart (Hacking Secret Ciphers with Python)
	while a != 0:
		a, b = b % a, a
	return b

def findModInverse(a, m):
	# Returns the modular inverse of a % m, which is
	# the number x such that a*x % m = 1
	# Author: Al Sweigart (Hacking Secret Ciphers with Python)
	if gcd(a, m) != 1:
		return None # no mod inverse if a and m aren't relatively prime

	# Calculate using the extended Euclidean algorithm
	u1, u2, u3 = 1, 0, a
	v1, v2, v3 = 0, 1, m
	while v3 != 0:
		q = u3 // v3
		v1, v2, v3, u1, u2, u3 = (u1 - q * v1), (u2 - q * v2), (u3 - q * v3), v1, v2, v3
	return u1 % m

def cipherLetterToOrdinal(letter):
	# 'A' translates to 0, 'B' to 1 etc.
	""" (str) -> integer
	
	Return the numeric value of the passed letter in the alphabet
	
	>>>  cipherLetterToOrdinal('A')
	0
	>>>  cipherLetterToOrdinal('a')
	0
	>>>  cipherLetterToOrdinal('Z')
	25
	>>>  cipherLetterToOrdinal('z')
	25
	"""
	return ord(letter.upper()) - 65

def ordinalToClearLetter(ordinal):
	# 0 translates to 'a', 1 to 'b' etc
	""" (integer) -> str
	
	Return the lowercase letter at the nth position in the alphabet (0 translates to 'a', 1 to 'b' etc)
	
	>>> ordinalToClearLetter(0)
	'a'
	>>> ordinalToClearLetter(25)
	'z'
	"""
	return chr(ordinal + 97)

def integerToChr(cipherInt):
	# Converts a mod 26 integer to a upper case character between A..Z
	""" (integer) -> str
	
	Convert a mod 26 integer to a upper case character between A..Z
	
	>>> integerToChr(7)
	'H'
	"""
	return chr(cipherInt + 65)

def stripWhitespace(string):
	# Returns the passed string, with all whitepace removed
	""" (str) -> str
	
	Return the passed string, with all whitespace removed
	
	>>> stripWhitespace('A B C D E F')
	'ABCDEF'
	"""
	return ''.join(string.split())

def frequencyAnalysis(charList):
	# Returns a dictionary of characters and their frequency in charList
	""" (list) -> dictionary
	
	Return a dictionary of characters and their frequency in charList
	
	>>> frequencyAnalysis(['X', 'S', 'F', 'J', 'D', 'J', 'M', 'N', 'R', 'F', 'R', 'U', 'D', 'J', 'V', 'L', 'M', 'Y', 'F', 'T', 'G', 'W', 'W', 'H', 'P', 'T', 'U', 'D', 'I', 'A', 'H', 'W', 'R', 'M', 'S', 'X', 'X', 'A', 'H', 'J', 'D', 'N', 'B', 'R', 'H', 'Q', 'T', 'O', 'F', 'F', 'N', 'W', 'F', 'G', 'H', 'G', 'L', 'D', 'J', 'J', 'A', 'T', 'Q', 'W', 'H', 'U', 'E', 'Q', 'E', 'M', 'D', 'M', 'H', 'R', 'H', 'L', 'M', 'C', 'G', 'L', 'Z', 'A', 'Y', 'B', 'T', 'H', 'U', 'W', 'I', 'C', 'M', 'H', 'D', 'J', 'I', 'C', 'G', 'F', 'V', 'Z', 'T', 'J', 'H', 'W', 'R', 'F', 'Y', 'B', 'X', 'B', 'H', 'T', 'T', 'L', 'X', 'A', 'H', 'F', 'L', 'Y', 'M', 'H', 'D', 'K', 'M', 'Z', 'K', 'T', 'P', 'S', 'S', 'U', 'M', 'R', 'H', 'F', 'H', 'L', 'R', 'U', 'W', 'A', 'T', 'H', 'U', 'J', 'V', 'L', 'T', 'Q', 'L', 'Z', 'S', 'G', 'S', 'N', 'A', 'F', 'W', 'L', 'W', 'U', 'G', 'X', 'D', 'U', 'Y', 'C', 'H', 'S', 'W', 'Z', 'J', 'W', 'H', 'S', 'I', 'A', 'I', 'Y', 'G', 'Y', 'L', 'S', 'Q', 'C', 'M', 'D', 'D', 'F', 'I', 'M', 'X', 'H', 'X', 'J', 'N', 'N', 'R', 'Y', 'R', 'E', 'F', 'E', 'X', 'N', 'W', 'H', 'T', 'M', 'L', 'N', 'E', 'D', 'J', 'C', 'Y', 'D', 'R', 'M', 'H', 'I', 'G', 'X', 'L', 'V', 'J', 'L', 'X', 'Q', 'H', 'U', 'Y', 'L', 'H', 'S', 'L', 'U', 'Y', 'L', 'T', 'S', 'V', 'S', 'H', 'N', 'B', 'T', 'Q', 'K', 'F', 'H', 'W', 'T', 'Q', 'D', 'N', 'H', 'X', 'U', 'D', 'Q', 'R', 'Y', 'G', 'Y', 'V', 'S', 'Q', 'F', 'M', 'M', 'R', 'K', 'J', 'Q', 'H', 'Z', 'O', 'V', 'S', 'I', 'M', 'G', 'H', 'H', 'T', 'M', 'L', 'N', 'E', 'D', 'J', 'Q', 'B', 'Y', 'K', 'G', 'Z', 'N', 'X', 'S', 'F', 'J', 'D', 'J', 'M', 'N', 'R', 'F', 'X', 'U', 'B', 'I', 'G', 'J', 'R', 'U', 'K', 'P', 'P', 'S', 'S', 'O', 'E', 'N', 'V', 'S', 'X', 'Y', 'G', 'N', 'R', 'J', 'Q', 'Y', 'V', 'Y', 'X', 'J', 'J', 'L', 'B', 'S', 'F', 'J', 'D', 'J', 'M', 'T', 'J', 'J', 'F', 'J', 'A', 'D', 'D', 'L', 'Y', 'B', 'X', 'Z', 'Q', 'A', 'A', 'Y', 'K', 'X', 'L', 'L', 'D', 'I', 'Y', 'X', 'X', 'J', 'W', 'Y', 'R', 'F', 'W', 'A', 'Y', 'M', 'L', 'N', 'P', 'H', 'Q', 'Y', 'L', 'Y', 'H', 'F', 'H', 'L', 'R', 'U', 'W', 'A', 'T', 'H', 'B', 'X', 'D', 'D', 'Q', 'U', 'U', 'T', 'X', 'L', 'Y', 'L', 'T', 'S', 'V', 'X', 'T', 'L', 'F', 'N', 'Q', 'Y', 'N', 'H', 'M', 'J', 'O', 'D', 'N', 'A', 'B', 'G', 'O', 'W', 'S', 'O', 'F', 'G', 'H', 'J', 'X', 'I', 'K', 'Y', 'H', 'P', 'Y', 'M', 'H', 'Z', 'Q', 'V', 'X', 'U', 'G', 'I', 'L', 'E', 'F', 'A', 'X', 'X', 'L', 'F', 'Y', 'I', 'T', 'X', 'W', 'J', 'J', 'U', 'F', 'T', 'I', 'F', 'T', 'H', 'L', 'J', 'Q', 'K', 'J', 'N', 'A', 'J', 'U', 'W', 'F', 'L', 'X', 'R', 'D', 'F', 'D', 'G', 'T', 'S', 'B', 'O', 'F', 'S', 'L', 'Y', 'R', 'H', 'J', 'L', 'Y', 'T', 'U', 'E', 'Y', 'B', 'T', 'Y', 'W', 'J', 'F', 'H', 'L', 'K', 'R', 'J', 'R', 'U', 'M', 'N', 'R', 'F', 'X', 'I', 'F', 'J', 'V', 'L', 'W', 'U', 'B', 'L', 'K', 'L', 'K', 'I', 'K', 'B', 'D', 'J', 'I', 'U', 'G', 'I', 'V', 'G', 'R', 'Y', 'O', 'J', 'U', 'Q', 'H', 'I', 'F', 'U', 'O', 'W', 'C', 'G', 'H', 'X', 'W', 'A', 'S', 'P', 'H', 'Q', 'Y', 'W', 'X', 'Q', 'T', 'U', 'S', 'A', 'S', 'A', 'E', 'J', 'W', 'L', 'J', 'L', 'L', 'K', 'R', 'J', 'S', 'O', 'F', 'G', 'H', 'J', 'X', 'U', 'G', 'I', 'X', 'K', 'J', 'G', 'T', 'Y', 'K', 'K', 'Y', 'I', 'W', 'T', 'W', 'Z', 'J', 'N', 'K', 'F', 'Q', 'K', 'K', 'I', 'K', 'R', 'D', 'L', 'N', 'I', 'G', 'M', 'R', 'O', 'J', 'P', 'X', 'W', 'Q', 'G', 'R', 'U', 'M', 'Y', 'H', 'J', 'B', 'B', 'B', 'H', 'K', 'E', 'J', 'N', 'A', 'T', 'G', 'A', 'X', 'O', 'L', 'J', 'G', 'L', 'M', 'Y', 'K', 'J', 'V', 'M', 'Q', 'N', 'B', 'S', 'J', 'K', 'H', 'L', 'T', 'R', 'E', 'D', 'J', 'X', 'W', 'F', 'W', 'S', 'X', 'N', 'K', 'J', 'D', 'E', 'X', 'B', 'H', 'Z', 'O', 'V', 'L', 'C', 'O', 'J', 'Q', 'G', 'M', 'C', 'G', 'Y', 'V', 'S', 'G', 'I', 'N', 'Y', 'K', 'G', 'B', 'C', 'M', 'B', 'D', 'K', 'J', 'H', 'V', 'W', 'B', 'H', 'Y', 'Y', 'W', 'I', 'X', 'J', 'N', 'H', 'Z', 'B', 'R', 'J', 'Q', 'X', 'P', 'F', 'U', 'A', 'N', 'N', 'A', 'J', 'D', 'D', 'Q', 'C', 'X', 'X', 'V', 'U', 'T', 'L', 'X', 'I', 'V', 'G', 'R', 'Y', 'G', 'T', 'W', 'S', 'G', 'F', 'X', 'A', 'L', 'U', 'Y', 'I', 'K', 'N', 'H', 'K', 'F', 'A', 'T', 'N', 'Q', 'K', 'Y', 'N', 'A', 'J', 'J', 'W', 'W', 'G', 'T', 'S', 'V', 'T', 'J', 'W', 'T', 'Z', 'V', 'W', 'Y', 'B', 'X', 'N', 'U', 'W', 'S', 'W', 'K', 'D', 'S', 'L', 'N', 'I', 'G', 'X', 'B', 'K', 'Y', 'Y', 'F', 'X', 'G', 'A', 'I', 'H', 'H', 'Y', 'V', 'M', 'K', 'Z', 'B', 'H', 'L', 'W', 'S', 'N', 'E', 'D', 'V', 'U', 'W', 'U', 'F', 'G', 'O', 'W', 'R', 'Y', 'L', 'X', 'D', 'Y', 'J', 'M', 'K', 'N', 'J', 'G', 'W', 'I', 'N', 'X', 'P', 'S', 'Y', 'B', 'X', 'R', 'D', 'L', 'N', 'W', 'T', 'Q', 'D', 'F', 'F', 'F', 'R', 'X', 'L', 'K', 'G', 'S', 'T', 'Q', 'O', 'A', 'J', 'X', 'V', 'T', 'G', 'W', 'H', 'L', 'T', 'H', 'N', 'W', 'W', 'M', 'E', 'F', 'L', 'V', 'G', 'U', 'K', 'J', 'S', 'S', 'Y', 'N', 'X', 'W', 'Q', 'K', 'M', 'C', 'W', 'I', 'H', 'F', 'B', 'C', 'M', 'M', 'L', 'F', 'Y', 'B', 'X', 'R', 'H', 'K', 'X', 'U', 'Z', 'J', 'V', 'S', 'S', 'X', 'N', 'X', 'H', 'V', 'Y', 'B', 'X', 'R', 'W', 'G', 'W', 'Y', 'V', 'W', 'H', 'S', 'Y', 'Y', 'M', 'M', 'H', 'E', 'F', 'W', 'A', 'N', 'Q', 'W', 'Z', 'M', 'X', 'I', 'W', 'G', 'J', 'H', 'V', 'W', 'B', 'H', 'Y', 'N', 'A', 'J', 'P', 'L', 'M', 'I', 'L', 'J', 'F', 'G', 'I', 'Y', 'L', 'W', 'H', 'N', 'T', 'F', 'O', 'J', 'G', 'S', 'W', 'I', 'N', 'S', 'G', 'L', 'M', 'Y', 'N', 'X', 'H', 'G', 'K', 'M', 'X', 'H', 'U', 'W', 'Y', 'E', 'X', 'D', 'V', 'L', 'M', 'U', 'M', 'B', 'H', 'J', 'J', 'M', 'A', 'F', 'U', 'W', 'I', 'U', 'F', 'T', 'Q', 'Y', 'Y', 'B', 'H', 'X', 'H', 'O', 'M', 'I', 'G', 'J', 'H', 'V', 'J', 'X', 'M', 'T', 'F', 'G', 'R', 'G', 'N', 'S', 'L', 'U', 'F', 'N', 'X', 'X', 'H', 'U', 'Z', 'L', 'X', 'Q', 'B', 'L', 'M', 'Y', 'L', 'J', 'D', 'J', 'J', 'E', 'G', 'T', 'Z', 'F', 'F', 'M', 'L', 'D', 'P', 'E', 'J', 'N', 'K', 'N', 'F', 'W', 'S', 'W', 'K', 'D', 'S', 'L', 'N', 'I', 'G', 'X', 'B', 'K', 'Y', 'Y', 'F', 'X', 'D', 'F', 'I', 'B', 'T', 'A', 'H', 'S', 'B', 'Y', 'T', 'P', 'Q', 'W', 'X', 'M', 'B', 'S', 'W', 'Z', 'F', 'N', 'X', 'A', 'H', 'J', 'D', 'I', 'G', 'J', 'L', 'F', 'A', 'I', 'E', 'A', 'H', 'V', 'M', 'U', 'L', 'Y', 'R', 'H', 'T', 'M', 'L', 'J', 'V', 'K', 'Y', 'B', 'X', 'X', 'D', 'E', 'J', 'M', 'X', 'Y', 'R', 'X', 'X', 'Y', 'V', 'W', 'H', 'L', 'P', 'Y', 'R', 'X'])
	{'U': 44, 'W': 66, 'O': 18, 'X': 78, 'V': 34, 'J': 83, 'B': 40, 'Y': 74, 'M': 53, 'L': 71, 'D': 45, 'N': 53, 'F': 62, 'Z': 19, 'I': 41, 'G': 55, 'Q': 36, 'T': 49, 'P': 14, 'K': 43, 'H': 78, 'S': 49, 'C': 13, 'R': 40, 'E': 21, 'A': 35}
	"""
	charFrequencies = {}
	for char in charList:
		if char in charFrequencies:
			charFrequencies[char] += 1
		else:
			charFrequencies[char] = 1
	return charFrequencies

def sortedFrequency(charFrequencies):
	# Returns a sorted list of the frequency of characters from a dictionary containing the letters and their frequencies
	""" (dictionary) -> list
	
	Return a sorted list of the frequency of characters
	
	>>> sortedFrequency({'U': 44, 'W': 66, 'O': 18, 'X': 78, 'V': 34, 'J': 83, 'B': 40, 'Y': 74, 'M': 53, 'L': 71, 'D': 45, 'N': 53, 'F': 62, 'Z': 19, 'I': 41, 'G': 55, 'Q': 36, 'T': 49, 'P': 14, 'K': 43, 'H': 78, 'S': 49, 'C': 13, 'R': 40, 'E': 21, 'A': 35})
	[(83, ['J']), (78, ['X', 'H']), (74, ['Y']), (71, ['L']), (66, ['W']), (62, ['F']), (55, ['G']), (53, ['M', 'N']), (49, ['T', 'S']), (45, ['D']), (44, ['U']), (43, ['K']), (41, ['I']), (40, ['B', 'R']), (36, ['Q']), (35, ['A']), (34, ['V']), (21, ['E']), (19, ['Z']), (18, ['O']), (14, ['P']), (13, ['C'])]
	"""
	sortedFrequency = {}
	for char, freq in charFrequencies.items():
		if freq in sortedFrequency:
			sortedFrequency[freq].append(char)
		else:
			sortedFrequency[freq] = [char]
	return sorted(list(sortedFrequency.items()), reverse=True)

def ioc(charList):
	# Calculates the Index of Coincidence for the list of characters charList
	""" (list) -> float
	
	Calculate the Index of Coincidence for the list of characters charList
	
	>>> ioc(['X', 'S', 'F', 'J', 'D', 'J', 'M', 'N', 'R', 'F', 'R', 'U', 'D', 'J', 'V', 'L', 'M', 'Y', 'F', 'T', 'G', 'W', 'W', 'H', 'P', 'T', 'U', 'D', 'I', 'A', 'H', 'W', 'R', 'M', 'S', 'X', 'X', 'A', 'H', 'J', 'D', 'N', 'B', 'R', 'H', 'Q', 'T', 'O', 'F', 'F', 'N', 'W', 'F', 'G', 'H', 'G', 'L', 'D', 'J', 'J', 'A', 'T', 'Q', 'W', 'H', 'U', 'E', 'Q', 'E', 'M', 'D', 'M', 'H', 'R', 'H', 'L', 'M', 'C', 'G', 'L', 'Z', 'A', 'Y', 'B', 'T', 'H', 'U', 'W', 'I', 'C', 'M', 'H', 'D', 'J', 'I', 'C', 'G', 'F', 'V', 'Z', 'T', 'J', 'H', 'W', 'R', 'F', 'Y', 'B', 'X', 'B', 'H', 'T', 'T', 'L', 'X', 'A', 'H', 'F', 'L', 'Y', 'M', 'H', 'D', 'K', 'M', 'Z', 'K', 'T', 'P', 'S', 'S', 'U', 'M', 'R', 'H', 'F', 'H', 'L', 'R', 'U', 'W', 'A', 'T', 'H', 'U', 'J', 'V', 'L', 'T', 'Q', 'L', 'Z', 'S', 'G', 'S', 'N', 'A', 'F', 'W', 'L', 'W', 'U', 'G', 'X', 'D', 'U', 'Y', 'C', 'H', 'S', 'W', 'Z', 'J', 'W', 'H', 'S', 'I', 'A', 'I', 'Y', 'G', 'Y', 'L', 'S', 'Q', 'C', 'M', 'D', 'D', 'F', 'I', 'M', 'X', 'H', 'X', 'J', 'N', 'N', 'R', 'Y', 'R', 'E', 'F', 'E', 'X', 'N', 'W', 'H', 'T', 'M', 'L', 'N', 'E', 'D', 'J', 'C', 'Y', 'D', 'R', 'M', 'H', 'I', 'G', 'X', 'L', 'V', 'J', 'L', 'X', 'Q', 'H', 'U', 'Y', 'L', 'H', 'S', 'L', 'U', 'Y', 'L', 'T', 'S', 'V', 'S', 'H', 'N', 'B', 'T', 'Q', 'K', 'F', 'H', 'W', 'T', 'Q', 'D', 'N', 'H', 'X', 'U', 'D', 'Q', 'R', 'Y', 'G', 'Y', 'V', 'S', 'Q', 'F', 'M', 'M', 'R', 'K', 'J', 'Q', 'H', 'Z', 'O', 'V', 'S', 'I', 'M', 'G', 'H', 'H', 'T', 'M', 'L', 'N', 'E', 'D', 'J', 'Q', 'B', 'Y', 'K', 'G', 'Z', 'N', 'X', 'S', 'F', 'J', 'D', 'J', 'M', 'N', 'R', 'F', 'X', 'U', 'B', 'I', 'G', 'J', 'R', 'U', 'K', 'P', 'P', 'S', 'S', 'O', 'E', 'N', 'V', 'S', 'X', 'Y', 'G', 'N', 'R', 'J', 'Q', 'Y', 'V', 'Y', 'X', 'J', 'J', 'L', 'B', 'S', 'F', 'J', 'D', 'J', 'M', 'T', 'J', 'J', 'F', 'J', 'A', 'D', 'D', 'L', 'Y', 'B', 'X', 'Z', 'Q', 'A', 'A', 'Y', 'K', 'X', 'L', 'L', 'D', 'I', 'Y', 'X', 'X', 'J', 'W', 'Y', 'R', 'F', 'W', 'A', 'Y', 'M', 'L', 'N', 'P', 'H', 'Q', 'Y', 'L', 'Y', 'H', 'F', 'H', 'L', 'R', 'U', 'W', 'A', 'T', 'H', 'B', 'X', 'D', 'D', 'Q', 'U', 'U', 'T', 'X', 'L', 'Y', 'L', 'T', 'S', 'V', 'X', 'T', 'L', 'F', 'N', 'Q', 'Y', 'N', 'H', 'M', 'J', 'O', 'D', 'N', 'A', 'B', 'G', 'O', 'W', 'S', 'O', 'F', 'G', 'H', 'J', 'X', 'I', 'K', 'Y', 'H', 'P', 'Y', 'M', 'H', 'Z', 'Q', 'V', 'X', 'U', 'G', 'I', 'L', 'E', 'F', 'A', 'X', 'X', 'L', 'F', 'Y', 'I', 'T', 'X', 'W', 'J', 'J', 'U', 'F', 'T', 'I', 'F', 'T', 'H', 'L', 'J', 'Q', 'K', 'J', 'N', 'A', 'J', 'U', 'W', 'F', 'L', 'X', 'R', 'D', 'F', 'D', 'G', 'T', 'S', 'B', 'O', 'F', 'S', 'L', 'Y', 'R', 'H', 'J', 'L', 'Y', 'T', 'U', 'E', 'Y', 'B', 'T', 'Y', 'W', 'J', 'F', 'H', 'L', 'K', 'R', 'J', 'R', 'U', 'M', 'N', 'R', 'F', 'X', 'I', 'F', 'J', 'V', 'L', 'W', 'U', 'B', 'L', 'K', 'L', 'K', 'I', 'K', 'B', 'D', 'J', 'I', 'U', 'G', 'I', 'V', 'G', 'R', 'Y', 'O', 'J', 'U', 'Q', 'H', 'I', 'F', 'U', 'O', 'W', 'C', 'G', 'H', 'X', 'W', 'A', 'S', 'P', 'H', 'Q', 'Y', 'W', 'X', 'Q', 'T', 'U', 'S', 'A', 'S', 'A', 'E', 'J', 'W', 'L', 'J', 'L', 'L', 'K', 'R', 'J', 'S', 'O', 'F', 'G', 'H', 'J', 'X', 'U', 'G', 'I', 'X', 'K', 'J', 'G', 'T', 'Y', 'K', 'K', 'Y', 'I', 'W', 'T', 'W', 'Z', 'J', 'N', 'K', 'F', 'Q', 'K', 'K', 'I', 'K', 'R', 'D', 'L', 'N', 'I', 'G', 'M', 'R', 'O', 'J', 'P', 'X', 'W', 'Q', 'G', 'R', 'U', 'M', 'Y', 'H', 'J', 'B', 'B', 'B', 'H', 'K', 'E', 'J', 'N', 'A', 'T', 'G', 'A', 'X', 'O', 'L', 'J', 'G', 'L', 'M', 'Y', 'K', 'J', 'V', 'M', 'Q', 'N', 'B', 'S', 'J', 'K', 'H', 'L', 'T', 'R', 'E', 'D', 'J', 'X', 'W', 'F', 'W', 'S', 'X', 'N', 'K', 'J', 'D', 'E', 'X', 'B', 'H', 'Z', 'O', 'V', 'L', 'C', 'O', 'J', 'Q', 'G', 'M', 'C', 'G', 'Y', 'V', 'S', 'G', 'I', 'N', 'Y', 'K', 'G', 'B', 'C', 'M', 'B', 'D', 'K', 'J', 'H', 'V', 'W', 'B', 'H', 'Y', 'Y', 'W', 'I', 'X', 'J', 'N', 'H', 'Z', 'B', 'R', 'J', 'Q', 'X', 'P', 'F', 'U', 'A', 'N', 'N', 'A', 'J', 'D', 'D', 'Q', 'C', 'X', 'X', 'V', 'U', 'T', 'L', 'X', 'I', 'V', 'G', 'R', 'Y', 'G', 'T', 'W', 'S', 'G', 'F', 'X', 'A', 'L', 'U', 'Y', 'I', 'K', 'N', 'H', 'K', 'F', 'A', 'T', 'N', 'Q', 'K', 'Y', 'N', 'A', 'J', 'J', 'W', 'W', 'G', 'T', 'S', 'V', 'T', 'J', 'W', 'T', 'Z', 'V', 'W', 'Y', 'B', 'X', 'N', 'U', 'W', 'S', 'W', 'K', 'D', 'S', 'L', 'N', 'I', 'G', 'X', 'B', 'K', 'Y', 'Y', 'F', 'X', 'G', 'A', 'I', 'H', 'H', 'Y', 'V', 'M', 'K', 'Z', 'B', 'H', 'L', 'W', 'S', 'N', 'E', 'D', 'V', 'U', 'W', 'U', 'F', 'G', 'O', 'W', 'R', 'Y', 'L', 'X', 'D', 'Y', 'J', 'M', 'K', 'N', 'J', 'G', 'W', 'I', 'N', 'X', 'P', 'S', 'Y', 'B', 'X', 'R', 'D', 'L', 'N', 'W', 'T', 'Q', 'D', 'F', 'F', 'F', 'R', 'X', 'L', 'K', 'G', 'S', 'T', 'Q', 'O', 'A', 'J', 'X', 'V', 'T', 'G', 'W', 'H', 'L', 'T', 'H', 'N', 'W', 'W', 'M', 'E', 'F', 'L', 'V', 'G', 'U', 'K', 'J', 'S', 'S', 'Y', 'N', 'X', 'W', 'Q', 'K', 'M', 'C', 'W', 'I', 'H', 'F', 'B', 'C', 'M', 'M', 'L', 'F', 'Y', 'B', 'X', 'R', 'H', 'K', 'X', 'U', 'Z', 'J', 'V', 'S', 'S', 'X', 'N', 'X', 'H', 'V', 'Y', 'B', 'X', 'R', 'W', 'G', 'W', 'Y', 'V', 'W', 'H', 'S', 'Y', 'Y', 'M', 'M', 'H', 'E', 'F', 'W', 'A', 'N', 'Q', 'W', 'Z', 'M', 'X', 'I', 'W', 'G', 'J', 'H', 'V', 'W', 'B', 'H', 'Y', 'N', 'A', 'J', 'P', 'L', 'M', 'I', 'L', 'J', 'F', 'G', 'I', 'Y', 'L', 'W', 'H', 'N', 'T', 'F', 'O', 'J', 'G', 'S', 'W', 'I', 'N', 'S', 'G', 'L', 'M', 'Y', 'N', 'X', 'H', 'G', 'K', 'M', 'X', 'H', 'U', 'W', 'Y', 'E', 'X', 'D', 'V', 'L', 'M', 'U', 'M', 'B', 'H', 'J', 'J', 'M', 'A', 'F', 'U', 'W', 'I', 'U', 'F', 'T', 'Q', 'Y', 'Y', 'B', 'H', 'X', 'H', 'O', 'M', 'I', 'G', 'J', 'H', 'V', 'J', 'X', 'M', 'T', 'F', 'G', 'R', 'G', 'N', 'S', 'L', 'U', 'F', 'N', 'X', 'X', 'H', 'U', 'Z', 'L', 'X', 'Q', 'B', 'L', 'M', 'Y', 'L', 'J', 'D', 'J', 'J', 'E', 'G', 'T', 'Z', 'F', 'F', 'M', 'L', 'D', 'P', 'E', 'J', 'N', 'K', 'N', 'F', 'W', 'S', 'W', 'K', 'D', 'S', 'L', 'N', 'I', 'G', 'X', 'B', 'K', 'Y', 'Y', 'F', 'X', 'D', 'F', 'I', 'B', 'T', 'A', 'H', 'S', 'B', 'Y', 'T', 'P', 'Q', 'W', 'X', 'M', 'B', 'S', 'W', 'Z', 'F', 'N', 'X', 'A', 'H', 'J', 'D', 'I', 'G', 'J', 'L', 'F', 'A', 'I', 'E', 'A', 'H', 'V', 'M', 'U', 'L', 'Y', 'R', 'H', 'T', 'M', 'L', 'J', 'V', 'K', 'Y', 'B', 'X', 'X', 'D', 'E', 'J', 'M', 'X', 'Y', 'R', 'X', 'X', 'Y', 'V', 'W', 'H', 'L', 'P', 'Y', 'R', 'X'])
	0.04472688108370197
	"""
	logger.info('Calculating ioc for %s chars = %s' % (len(charList), ''.join(charList)))
	charFrequencies = frequencyAnalysis(charList)
	ioc = 0
	n = len(charList)
	for ordinal in (range(0, 26)):
		letter = ordinalToClearLetter(ordinal).upper()
		if letter in charFrequencies:
			F = charFrequencies[letter]
		else:
			F = 0
		iocLetter = (F**2 - F) / (n**2 - n)
		ioc += iocLetter
		logger.debug('%s : %s\t: cumulative: %s' % (letter, iocLetter, ioc))
	return ioc

def displayFrequency(sortedList):
	# Displays the sorted frequency list
	for item in sortedList:
		print('%s : %s' % (item[0], item[1]))

# Always perform a sanity check first on the known example cipher:
print('Checking logic on cipher_utils module...')
logger.setLevel(logger.Level.ERROR)
if integerToChr(7) != 'H':
	print('Error testing integerToChr(cipherInt) method!!! Check your code before continuing...')
	sys.exit()
else:
	print('logic OK.')
logger.setLevel(logger.Level.ERROR)

# if cipher_utils.py is run, instead of being imported as a module,
# call the main() function

if __name__ == '__main__':
	main()
