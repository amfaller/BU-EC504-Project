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


# defaultdict is used only for storing the final output
# We will return a dictionary where key is the matched word
# and value is the list of indexes of matched word
from collections import defaultdict

# re is a regex-matching library that aids in wildcard search.
import regex

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
        self.out = [0] * (self.max_states + 1)

        # FAILURE FUNCTION IS IMPLEMENTED USING fail []
        # There is one value for each state + 1 for the root
        # It has been initialized to all -1
        # This will contain the fail state value for each state
        self.fail = [-1] * (self.max_states + 1)

        # GOTO FUNCTION (OR TRIE) IS IMPLEMENTED USING goto [[]]
        # Number of rows = max_states + 1
        # Number of columns = max_characters i.e 26 in our case
        # It has been initialized to all -1.
        self.goto = [[-1] * self.max_characters for _ in range(self.max_states + 1)]

        # Convert all words to lowercase
        # so that our search is case insensitive
        for i in range(len(words)):
            words[i] = words[i].lower()

        # This character represents a wildcard.
        self.wildcard = '*'

        # All the words in dictionary which will be used to create Trie
        # The index of each keyword is important:
        # "out[state] & (1 << i)" is > 0 if we just found word[i]
        # in the text.
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

    # Builds the String matching machine.
    # Returns the number of states that the built machine has.
    # States are numbered 0 up to the return value - 1, inclusive.
    def __build_matching_machine(self):
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
                ch = ord(character) - 97  # Ascii value of 'a' = 97

                # Allocate a new node (create a new state)
                # if a node for ch doesn't exist.
                if self.goto[current_state][ch] == -1:
                    self.goto[current_state][ch] = states
                    states += 1

                current_state = self.goto[current_state][ch]

            # Add current word in output function
            self.out[current_state] |= (1 << i)

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
        ch = ord(next_input) - 97  # Ascii value of 'a' is 97

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

        # Handle wildcard words
        for word in self.wildcardWords:
            self.findWildcardMatch(result, text, word)

        # Traverse the text through the built machine
        # to find all occurrences of words
        for i in range(len(text)):
            current_state = self.__find_next_state(current_state, text[i])

            # If match not found, move to next state
            if self.out[current_state] == 0: continue

            # Match found, store the word in result dictionary
            for j in range(len(self.words)):
                if (self.out[current_state] & (1 << j)) > 0:
                    word = self.words[j]

                    # Start index of word is (i-len(word)+1)
                    result[word].append(i - len(word) + 1)

        # Return the final result dictionary
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
    
def outputTestCase(text, words, caseString, expectedOutput):
        case = "\n\n== {caseString} ".format(caseString=caseString)
        case = case.ljust(85,"=")
        print(case, "\n")

        aho_chorasick = AhoCorasick(words)
        result = aho_chorasick.search_words(text)

        print(" > Search words:")
        print(words)
        print("\n > Text:")
        print(text)
    
        print("\n > Results:")
        for word in result:
            if word.isalpha():
                for i in result[word]:
                    print(" - Word", text[i:i+len(word):1], "appears from index", i, "to", i+len(word)-1)
        print("\n > Expected:")
        print(expectedOutput)

# Driver code
if __name__ == "__main__":
    caseList = ["Sample Test Case", "Test Case: Wildcards at Beginning / End of Search Words", "Test Case: Capitalization", "Test Case: Word Overlap"]
    wordsList = [["hers", "h*s", "p*t", "p**t"], ["**ing", "hors*", "ol*", "*oad"], ["thou", "sand", "thousand", "i ", "the", "CAN"], ["veg", "get", "table", "tab", "able", "vegetable"]]
    textStringList = ["ahishers pets peterpptttr", "I am going to take my horse to that old town road and I am going to ride until I can no longer", "ThouSand miLes from Shore, I cAN float on THE water", "vegetable"]
    expectedOutList = [" - Word his appears from index 1 to 3\n - Word pet appears from index 9 to 11\n - Word pet appears from index 14 to 16\n - Word ppt appears from index 19 to 21\n - Word ptt appears from index 20 to 22\n - Word pptt appears from index 19 to 22\n - Word pttt appears from index 20 to 23\n - Word hers appears from index 4 to 7",
      " - Word going appears from index 5 to 9\n - Word going appears from index 59 to 63\n - Word horse appears from index 22 to 26\n - Word old appears from index 36 to 38\n - Word road appears from index 45 to 48",
      " - Word Thou appears from index 0 to 3\n - Word Sand appears from index 4 to 7\n - Word ThouSand appears from index 0 to 7\n - Word cAN appears from index 29 to 31\n - Word THE appears from index 42 to 44",
      " - Word veg appears from index 0 to 2\n - Word get appears from index 2 to 4\n - Word tab appears from index 4 to 6\n - Word table appears from index 4 to 8\n - Word able appears from index 5 to 8\n - Word vegetable appears from index 0 to 8"]
    for i in range(len(caseList)):
        outputTestCase(textStringList[i], wordsList[i], caseList[i], expectedOutList[i])
