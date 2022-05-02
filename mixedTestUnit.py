import unittest
from AhoCorasick import AhoCorasick

class Test(unittest.TestCase):
    text = "CatDdcabirg bIRdscaabird snaKsncKsAt ssnakESbirdog dsccaTdg";
    words = ["c**", "b*R*", "sn*kS", "c**d*", "D*cA**", "S*NAKES", "s******"]
    testClass = AhoCorasick(words)
    result = testClass.search_words(text)
    testResult = list(result)

    def test0(self):
        print("\nStart test 0 for first word 'c**'\n")

        self.assertEqual(self.testResult[0], self.text[0:3])
        self.assertEqual(self.testResult[1], self.text[5:8])
        self.assertEqual(self.testResult[2], self.text[17:20])
        self.assertEqual(self.testResult[3], self.text[31:34])
        self.assertEqual(self.testResult[4], self.text[53:56])
        self.assertEqual(self.testResult[5], self.text[54:57])

        print("\nFinish test 0")
    
    def test1(self):
        print("\nStart test 1 for first word 'b*R*'\n")

        self.assertEqual(self.testResult[6], self.text[7:11])
        self.assertEqual(self.testResult[7], self.text[12:16])
        self.assertEqual(self.testResult[8], self.text[20:24])
        self.assertEqual(self.testResult[8], self.text[44:48])

        print("\nFinish test 1")

    def test2(self):
        print("\nStart test 2 for first word 'sn*kS'\n")

        self.assertEqual(self.testResult[9], self.text[25:30])
        self.assertEqual(self.testResult[10], self.text[29:34])

        print("\nFinish test 2")
    
    def test3(self):
        print("\nStart test 3 for first word 'c**d*'\n")

        self.assertEqual(self.testResult[11], self.text[0:5])
        self.assertEqual(self.testResult[12], self.text[54:59])

        print("\nFinish test 3")

    def test4(self):
        print("\nStart test 4 for first word 'D*cA**'\n")

        self.assertEqual(self.testResult[13], self.text[3:9])
        self.assertEqual(self.testResult[14], self.text[15:21])

        print("\nFinish test 4")

    def test5(self):
        print("\nStart test 4 for first word 'S*NAKES'\n")

        self.assertEqual(self.testResult[15], self.text[37:44])

        print("\nFinish test 5")

    def test6(self):
        print("\nStart test 6 for first word 's******'\n")
        
        self.assertEqual(self.testResult[16], self.text[16:23])
        self.assertEqual(self.testResult[17], self.text[25:32])
        self.assertEqual(self.testResult[18], self.text[29:36])
        self.assertEqual(self.testResult[19], self.text[38:45])
        self.assertEqual(self.testResult[20], self.text[43:50])
        self.assertEqual(self.testResult[21], self.text[52:59])

        print("\nFinish test 6")
   
if __name__ == '__main__':
    # Begin unittest.main()
    unittest.main()