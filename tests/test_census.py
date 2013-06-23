import unittest
import json
from dataomega.census import SimpleCensusParser

class TestSimpleCensusParser(unittest.TestCase):
    def setUp(self):
        self.parser = SimpleCensusParser()
    
    def test_a_question(self):
        q = 'how many Dominicans in New York?'
        match = self.parser.search(q)
        self.assertIsNotNone(match)
        
        self.assertIsNotNone(match.as_json())
        d = json.loads(match.as_json())
        self.assertEquals('04000US36',d['place']['full_geoid'])
        self.assertEquals(695158,d['population'])
        
        q = "how many chileans in new york?"
        match = self.parser.search(q)
        self.assertIsNotNone(match)
        
        self.assertIsNotNone(match.as_json())
        d = json.loads(match.as_json())
        self.assertEquals('04000US36',d['place']['full_geoid'])
        self.assertEquals(16764,d['population'])
        
        
