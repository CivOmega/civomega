import unittest

from dataomega.census import SimpleCensusParser

class TestSimpleCensusParser(unittest.TestCase):
    def setUp(self):
        self.parser = SimpleCensusParser()
    
    def test_a_question(self):
        q = 'how many Dominicans in New York?'
        match = self.parser.search(q)
        self.assertIsNotNone(match)
    
