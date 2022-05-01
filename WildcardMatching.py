# Sample program to demonstrate re functionality.
# Author: Tony Faller
#
# https://www.geeksforgeeks.org/python-wildcard-substring-search/
# https://www.tutorialspoint.com/How-do-we-use-re-finditer-method-in-Python-regular-expression

import re

def findWildcardMatch(text, pattern):
	print("The original string is : " + text)
	subStr = pattern.replace("*", ".")

	# Compile wildcard word to regex
	regexPat = re.compile(subStr)

	# Use re.finditer() to get match and indices
	for match in re.finditer(regexPat, text):
		start = match.start()
		end = match.end()
		print("String match " + text[start:end] + " at [" + str(start) + ":" + str(end) + "]")


if __name__ == "__main__":
    words = ["he", "she", "hers", "h*s"]
    text = "ahishers"
  
    # Create an Object to initialize the Trie
    for word in words:
    	if '*' in word:
    		findWildcardMatch(text, word)
