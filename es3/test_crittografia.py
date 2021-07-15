import unittest

import crittografia

alphabet=['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',' ']

class test_crittografia (unittest.TestCase):

    def test_Vigenere(self):
        message="edoardo casa"
        key="pippo"
        critt_message=crittografia.critt_Vigenere(message,key)
        #print(critt_message)
        solution="tlcpesworogi"
        self.assertEqual(critt_message,solution)
        decritt_message=crittografia.decritt_Vigenere(critt_message,key)
        self.assertEqual(message,decritt_message)

if __name__ == '__main__': 
    unittest.main()