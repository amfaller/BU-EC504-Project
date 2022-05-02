###############################################################################################
# As was answered in Piazza (question @249), the use
# of incomplete implementations are allowed.
#
# This implementation of Aho-Corasick was sourced from: 
# https://www.geeksforgeeks.org/aho-corasick-algorithm-pattern-searching/
#
# Implementations of wildcard string matching may be found here:
# https://www.geeksforgeeks.org/python-wildcard-substring-search/
# https://www.tutorialspoint.com/How-do-we-use-re-finditer-method-in-Python-regular-expression
#
# These implementations were combined to complete the goal of this project.
###############################################################################################

from collections import defaultdict

# re is a regex-matching library that aids in wildcard search.
import regex

class AhoCorasick:
    def __init__(self, words):
  
        # Max number of states in the matching machine
        self.max_states = sum([len(word) for word in words])
  
        # Maximum number of characters
        self.max_characters = 128
  
        # OUTPUT FUNCTION IS IMPLEMENTED USING out []
        self.out = [0]*(self.max_states+1)
  
        # FAILURE FUNCTION IS IMPLEMENTED USING fail []
        self.fail = [-1]*(self.max_states+1)
  
        # GOTO FUNCTION (OR TRIE) IS IMPLEMENTED USING goto [[]]
        self.goto = [[-1]*self.max_characters for _ in range(self.max_states+1)]
          
        # Convert all words to lowercase
        # so that our search is case insensitive
        for i in range(len(words)):
          words[i] = words[i].lower()

        # This character represents a wildcard
        self.wildcard = '*'
            
        # All the words in dictionary which will be used to create Trie
        self.words = []
        self.wildcardWords = []
        for word in words:
            if self.wildcard in word:
                self.wildcardWords.append(word)
            else:
                self.words.append(word)

        # Once the Trie has been built, it will contain the number
        # of nodes in Trie which is total number of states required <= max_states
        self.states_count = self.__build_matching_machine()

    # Builds the String matching machine
    def __build_matching_machine(self):
        k = len(self.words)
  
        states = 1
  
        for i in range(k):
            word = self.words[i]
            current_state = 0
  
            for character in word:
                ch = ord(character) - 97
  
                # Allocate a new node (create a new state)
                # if a node for ch doesn't exist.
                if self.goto[current_state][ch] == -1:
                    self.goto[current_state][ch] = states
                    states += 1
  
                current_state = self.goto[current_state][ch]
  
            # Add current word in output function
            self.out[current_state] |= (1<<i)
  
        # For all characters which don't have
        # an edge from root (or state 0) in Trie,
        # add a goto edge to state 0 itself
        for ch in range(self.max_characters):
            if self.goto[0][ch] == -1:
                self.goto[0][ch] = 0
          
        # Failure function is computed in 
        # breadth first order using a queue
        queue = []
  
        for ch in range(self.max_characters):
            if self.goto[0][ch] != 0:
                self.fail[self.goto[0][ch]] = 0
                queue.append(self.goto[0][ch])
  
        while queue:
            state = queue.pop(0)
  
            # For the removed state, find failure
            # function for all those characters
            # for which goto function is not defined.
            for ch in range(self.max_characters):
  
                # If goto function is defined for
                # character 'ch' and 'state'
                if self.goto[state][ch] != -1:
  
                    # Find failure state of removed state
                    failure = self.fail[state]
  
                    # Find the deepest node labeled by proper
                    # suffix of String from root to current state.
                    while self.goto[failure][ch] == -1:
                        failure = self.fail[failure]
                      
                    failure = self.goto[failure][ch]
                    self.fail[self.goto[state][ch]] = failure
  
                    # Merge output values
                    self.out[self.goto[state][ch]] |= self.out[failure]
  
                    queue.append(self.goto[state][ch])
          
        return states
  
    # Returns the next state the machine will transition to using goto
    # and failure functions
    def __find_next_state(self, current_state, next_input):
        answer = current_state
        ch = ord(next_input) - 97
  
        # If goto is not defined, use failure function
        while self.goto[answer][ch] == -1:
            answer = self.fail[answer]
  
        return self.goto[answer][ch]
  
    # This function finds all occurrences of all words in text.
    def search_words(self, text):
        current_state = 0
  
        result = defaultdict(list)

        # Handle wildcard words
        for word in self.wildcardWords:
            self.findWildcardMatch(result, text, word)
  
        # Traverse the text through the built machine to find all occurrences of words
        for i in range(len(text)):
            current_state = self.__find_next_state(current_state, text[i])
  
            # If match not found, move to next state
            if self.out[current_state] == 0: continue
  
            # Match found, store the word in result dictionary
            for j in range(len(self.words)):
                if (self.out[current_state] & (1<<j)) > 0:
                    word = self.words[j]
  
                    result[word].append(i-len(word)+1)

        # # Remove potential duplicate values for each word
        # result = { key : list(set(value)) for key, value in result.items()}

        return result

    # This function handles all occurrences of words containing wildcards.
    def findWildcardMatch(self, outputDict, text, pattern):
        # Replace our wildcard with regex wildcard
        subStr = pattern.replace(self.wildcard, ".")

        # Compile wildcard word to regex
        regexPat = regex.compile(subStr)
        
        # Use re.finditer() to get match and indices
        for match in regex.finditer(regexPat, text.lower(), overlapped=True):
            # Remove any matches with spaces
            if bool(regex.search(r"\s", match.group())):
                continue
            
            start = match.start()
            end = match.end()
            outputDict[text[start:end]].append(start)