#############################################################################
# As was answered in Piazza (question @249), the use
# of incomplete implementations are allowed.
#
# This implementation of Aho-Corasick was sourced from: 
# https://www.geeksforgeeks.org/aho-corasick-algorithm-pattern-searching/
#############################################################################


# Python program for implementation of
# Aho-Corasick algorithm for string matching
  
# defaultdict is used only for storing the final output
# We will return a dictionary where key is the matched word
# and value is the list of indexes of matched word
from collections import defaultdict

# Character representing wildcard.
# ASSUMPTION: 1 wildcard per search word
wildcard = '*'
  
# For simplicity, Arrays and Queues have been implemented using lists. 
# If you want to improve performance try using them instead
class AhoCorasick:
    def __init__(self, words):
  
        # Max number of states in the matching machine.
        # Should be equal to the sum of the length of all keywords.
        self.max_states = sum([len(word) for word in words])
  
        # Maximum number of characters.
        # Currently supports only alphabets [a,z]
        self.max_characters = 128
  
        # OUTPUT FUNCTION IS IMPLEMENTED USING out []
        # Bit i in this mask is 1 if the word with
        # index i appears when the machine enters this state.
        # Lets say, a state outputs two words "he" and "she" and
        # in our provided words list, he has index 0 and she has index 3
        # so value of out[state] for this state will be 1001
        # It has been initialized to all 0.
        # We have taken one extra state for the root.
        self.out = [0]*(self.max_states+1)
  
        # FAILURE FUNCTION IS IMPLEMENTED USING fail []
        # There is one value for each state + 1 for the root
        # It has been initialized to all -1
        # This will contain the fail state value for each state
        self.fail = [-1]*(self.max_states+1)
  
        # GOTO FUNCTION (OR TRIE) IS IMPLEMENTED USING goto [[]]
        # Number of rows = max_states + 1
        # Number of columns = max_characters i.e 26 in our case
        # It has been initialized to all -1.
        self.goto = [[-1]*self.max_characters for _ in range(self.max_states+1)]
          
        # Convert all words to lowercase
        # so that our search is case insensitive
        for i in range(len(words)):
          words[i] = words[i].lower()
            
        # All the words in dictionary which will be used to create Trie
        # The index of each keyword is important:
        # "out[state] & (1 << i)" is > 0 if we just found word[i]
        # in the text.
        self.words = words
        self.wildcard_words = []
        self.wildcard_substrings = []

        # for word in self.words:
        #     print(word)

        # This defaultdict contains the indices required for each wildcarded word's substrings.
        self.wildcard_substring_indices = defaultdict(list)
  
        # Once the Trie has been built, it will contain the number
        # of nodes in Trie which is total number of states required <= max_states
        self.states_count = self.__build_matching_machine()

    def __split_wildcard_words(self, wildword):
        # print("Passed word is " + wildword)
        # print("At time of splitting, word array is:")
        # for word in self.words:
        #     print("\t" + word)
        wildCardIndex = 0
        oldWildCardIndex = 0
        try:
            while wildword.index('*', wildCardIndex+1):
                wildCardIndex = wildword.index('*', wildCardIndex+1)
                self.words.append(wildword[oldWildCardIndex:wildCardIndex])
                # print(wildword[oldWildCardIndex:wildCardIndex])     # For debugging
                self.wildcard_substrings.append(wildword[oldWildCardIndex:wildCardIndex])
                self.wildcard_substring_indices[wildword[oldWildCardIndex:wildCardIndex]].append(oldWildCardIndex)
                oldWildCardIndex = wildCardIndex+1
        except Exception as e:
            oldWildCardIndex = wildCardIndex+1
            self.words.append(wildword[oldWildCardIndex::])
            self.wildcard_substrings.append(wildword[oldWildCardIndex::])
            self.wildcard_substring_indices[wildword[oldWildCardIndex::]].append(oldWildCardIndex)

        # print("Now, word array is:")
        # for word in self.words:
        #     print("\t" + word)

        # print(self.wildcard_substring_indices[wildword])

  
    # Builds the String matching machine.
    # Returns the number of states that the built machine has.
    # States are numbered 0 up to the return value - 1, inclusive.
    def __build_matching_machine(self):

        # Preprocess any wildcard-containing words to its substrings.
        # Remove the word from the search list, and replace it 
        # with its substrings.
        wordsLength = len(self.words)
        indexer = 0
        while indexer < wordsLength:
            # print("Checking word " + self.words[indexer])
            if wildcard in self.words[indexer]:
                # print("Wildcard found in " + self.words[indexer])
                self.wildcard_words.append(self.words[indexer])
                self.__split_wildcard_words(self.words[indexer])
                self.words.remove(self.words[indexer])
                wordsLength = len(self.words)
                indexer = 0
            else: indexer += 1


        k = len(self.words)
  
        # Initially, we just have the 0 state
        states = 1
  
        # Convalues for goto function, i.e., fill goto
        # This is same as building a Trie for words[]
        for i in range(k):
            word = self.words[i]
            current_state = 0
  
            # Process all the characters of the current word
            for character in word:
                ch = ord(character) - 97 # Ascii value of 'a' = 97

                if character == '*':
                    ch += 97
  
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
  
        # Iterate over every possible input
        for ch in range(self.max_characters):
  
            # All nodes of depth 1 have failure
            # function value as 0. For example,
            # in above diagram we move to 0
            # from states 1 and 3.
            if self.goto[0][ch] != 0:
                self.fail[self.goto[0][ch]] = 0
                queue.append(self.goto[0][ch])
  
        # Now queue has states 1 and 3
        while queue:
  
            # Remove the front state from queue
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
  
                    # Insert the next level node (of Trie) in Queue
                    queue.append(self.goto[state][ch])
          
        return states
  
  
    # Returns the next state the machine will transition to using goto
    # and failure functions.
    # current_state - The current state of the machine. Must be between
    #             0 and the number of states - 1, inclusive.
    # next_input - The next character that enters into the machine.
    def __find_next_state(self, current_state, next_input):
        answer = current_state
        ch = ord(next_input) - 97 # Ascii value of 'a' is 97
  
        # If goto is not defined, use
        # failure function
        while self.goto[answer][ch] == -1:
            answer = self.fail[answer]
  
        return self.goto[answer][ch]
  
  
    # This function finds all occurrences of all words in text.
    def search_words(self, text):
        # Convert the text to lowercase to make search case insensitive
        text = text.lower()
  
        # Initialize current_state to 0 
        current_state = 0
  
        # A dictionary to store the result.
        # Key here is the found word
        # Value is a list of all occurrences start index
        result = defaultdict(list)
  
        wordFound = True
        wildCardPossibleFlag = False
        firstSubstringIndex = -1
        indexInText = -1
        distance = 99999

        # Traverse the text through the built machine
        # to find all occurrences of words
        for i in range(len(text)):
            print("> Current index: " + str(i))
            current_state = self.__find_next_state(current_state, text[i])
  
            # If match not found, move to next state
            if self.out[current_state] == 0: continue
  
            # Match found, store the word in result dictionary
            # First check if this could be a wildcard substring match
            



            for j in range(len(self.words)):
                if (self.out[current_state] & (1<<j)) > 0:  # At this point in execution, we have confirmed that a match is found.

                    wordFound = True
                    word = self.words[j]

                    # for k in range(len(self.wildcard_substrings)):      # For debugging
                    #     print(" = " + self.wildcard_substrings[k])      # For debugging

                    # Search if the found word is a wildcard substring
                    for k in range(len(self.wildcard_substrings)):
                        # print("> Looking at " + self.words[j] + " vs " + self.wildcard_substrings[k])
                        if self.words[j] == self.wildcard_substrings[k]:
                            print(">> Looking at " + self.words[j] + " vs " + self.wildcard_substrings[k])
                            wordFound = False
                            # If the latter portion of a wildcard string and it completes a word, set word as detected
                            if wildCardPossibleFlag is True:
                                
                                # print(self.wildcard_substring_indices[self.words[j]][0])
                                # print(firstSubstringIndex[0])
                                # distance = self.wildcard_substring_indices[self.words[j]][0]-firstSubstringIndex[0]
                                if self.wildcard_substring_indices[self.words[j]][0]-firstSubstringIndex[0] == i-indexInText:
                                    print(" -  LATTER IS " + self.words[j])
                                    print("  - DIFF IN FIRST: " + str(self.wildcard_substring_indices[self.words[j]][0]-firstSubstringIndex[0]))      # For debugging
                                    print("  - DIFF IN SECOND: " + str(i-indexInText))
                                    # print(" - WORD FOUND!")
                                    word = text[indexInText:i+1]
                                    wildCardPossibleFlag = False
                                    firstSubstringIndex = -1
                                    indexInText = -1
                                    wordFound = True
                                elif self.wildcard_substring_indices[self.words[j]][0]-firstSubstringIndex[0] < i-indexInText:
                                    print("   - Limit reached, wildcard word not possible")
                                    word = text[indexInText:i+1]
                                    wildCardPossibleFlag = False
                                    firstSubstringIndex = -1
                                    indexInText = -1
                                    wordFound = False
                            # If the former portion of a wildcard string, set flags and continue
                            elif wildCardPossibleFlag is False:
                                print(" -  FORMER IS " + self.words[j])      # For debugging
                                wildCardPossibleFlag = True
                                wordFound = False
                                firstSubstringIndex = self.wildcard_substring_indices[self.words[j]]
                                indexInText = i
                                break

                            # # If out of range, reset all flags
                            # if distance < i-indexInText:
                            #     wildCardPossibleFlag = True
                            #     wordFound = False
                            #     distance = 99999
                            
                  
  
                    if wordFound is True:
                        print("    - APPENDED WORD IS " + word)
                    # Start index of word is (i-len(word)+1)
                        result[word].append(i-len(word)+1)
  
        # Return the final result dictionary
        return result
  
# Driver code
if __name__ == "__main__":
    words = ["he", "she", "hers", "h*s", "p*t"]
    text = "ahishers pets pepoterpotter"
  
    # Create an Object to initialize the Trie
    aho_chorasick = AhoCorasick(words)
  
    # Get the result
    result = aho_chorasick.search_words(text)
  
    # Print the result
    print("\n== RESULTS ==")
    for word in result:
        for i in result[word]:
            print("Word", word, "appears from", i, "to", i+len(word)-1)
