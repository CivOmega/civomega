import unittest
import json
from civomega.modules.census_population import SimpleCensusParser

class TestSimpleCensusParser(unittest.TestCase):
    def setUp(self):
        self.parser = SimpleCensusParser()

    def test_a_question(self):
        q = 'How many Dominicans live in New York?'
        matches = self.parser.search(q)
        self.assertIsNotNone(matches)
        self.assertIsNotNone(matches[0].as_json())
        d = json.loads(matches[0].as_json())
        self.assertEquals('04000US36',d['place']['full_geoid'])
        self.assertEquals(695158,d['population'])
        self.assertTrue('New York' in matches[0].as_html())
        self.assertTrue('695,158' in matches[0].as_html())

        q = "how many chileans live in new york city?"
        matches = self.parser.search(q)
        self.assertIsNotNone(matches)
        self.assertIsNotNone(matches[0].as_json())
        d = json.loads(matches[0].as_json())
        self.assertEquals('16000US3651000',d['place']['full_geoid'])
        self.assertEquals(8124,d['population'])


    def test_asian_questions(self):
        q = 'how many chinese are in New York?'
        matches = self.parser.search(q)
        self.assertIsNotNone(matches)

        self.assertIsNotNone(matches[0].as_json())
        d = json.loads(matches[0].as_json())
        self.assertEquals('04000US36',d['place']['full_geoid'])
        self.assertEquals(564836,d['population'])
        
