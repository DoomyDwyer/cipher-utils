# The Cipher Utils project #

Python utilities to help crack the ciphers from the National Cipher Challenge 2016 https://www.cipherchallenge.org/

A couple of the functions were authored by Al Sweigart in his book Hacking Secret Ciphers with Python http://inventwithpython.com/hacking/ His authorship is attributed in the code.

- `cipher_utils.py` contains the utility classes to help crack the ciphers
- The `main` function works through an example of cracking a Vigenère cipher
- Many functions contain docstring help texts:


	    >>>import cipher_utils
	    Checking decryption logic...
	    decryption logic OK.
	    >>>help(cipher_utils.ioc)
	    
	    Help on function ioc in module cipher_utils:
	    
	    ioc(charList)
	    (list) -> float
	    
	    Calculate the Index of Coincidence for the list of characters charList
	    
	    >>>ioc(['X', 'S', 'F', 'J', 'D', 'J', 'M', 'N', 'R', 'F', 'R', 'U', 'D', ... 'X', 'X', 'Y', 'V', 'W', 'H', 'L', 'P', 'Y', 'R', 'X'])
	    0.04472688108370197
	    
