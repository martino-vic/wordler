import unittest
from wordler import wordler

class Test1(unittest.TestCase):
    
    def test_cln(self):   
        self.assertEqual(wordler.cln("ABC*.=?#"), "abc")
        
    def test_cln2(self):
        instr="""Solutions:
penguin
giraffe
polar bear
"""
        self.assertEqual(wordler.cln2(instr), ["penguin", "giraffe", "polar bear", ""])
        
    def test_main(self):
        with patch('builtins.input', side_effect=["y", "n", "y"])
            pass