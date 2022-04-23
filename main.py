# Driver script to test trie functionality

from trie import Trie

t = Trie();

t.insert("was")
t.insert("word")
t.insert("war")
t.insert("what")
t.insert("where")

print(t.query("wh"))