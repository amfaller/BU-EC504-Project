from AhoCorasick import AhoCorasick

# Driver code
if __name__ == "__main__":
    print("===== Test Case: Mixture of Wild Cards and Varied Casing =====")

    text = "CatDdcabirg bIRdscaabird snaKsncKsAt ssnakESbirdog dsccaTdg";
    words = ["c**", "b*R*", "sn*kS", "c**d*", "D*cA**", "S*NAKES", "s******"]

    print("> Search words:")
    print(words)

    print("> Text:")
    print(text)
  
    # Create an Object to initialize the Trie
    aho_chorasick = AhoCorasick(words)
  
    # Get the result
    result = aho_chorasick.search_words(text)
    
    print("\n> Results:")
    # Print the result
    for word in result:
        for i in result[word]:
            print(" - Word", word, "appears from", i, "to", i+len(word)-1)

    print("\n> Expected:")
    print("- Word Cat appears from 0 to 2")
    print("- Word cab appears from 5 to 7")
    print("- Word caa appears from 17 to 19")
    print("- Word cKs appears from 31 to 33")
    print("- Word cca appears from 53 to 55")
    print("- Word caT appears from 54 to 56")
    print("- Word birg appears from 7 to 10")
    print("- Word bIRd appears from 12 to 15")
    print("- Word bird appears from 20 to 23")
    print("- Word bird appears from 44 to 47")
    print("- Word snaKs appears from 25 to 29")
    print("- Word sncKs appears from 29 to 33")
    print("- Word CatDd appears from 0 to 4")
    print("- Word caTdg appears from 54 to 58")
    print("- Word Ddcabi appears from 3 to 8")
    print("- Word dscaab appears from 15 to 20")
    print("- Word ssnakES appears from 37 to 43")
    print("- Word ssnakES appears from 37 to 43")
    print("- Word scaabir appears from 16 to 22")
    print("- Word snaKsnc appears from 25 to 31")
    print("- Word sncKsAt appears from 29 to 35")
    print("- Word snakESb appears from 38 to 44")
    print("- Word Sbirdog appears from 43 to 49")
    print("- Word sccaTdg appears from 52 to 58")