from dataomega import Parser, Match

import re

import requests

SIMPLE_PATTERN = re.compile('^\s*(?:how many|how much|which are|which)(?P<noun>.+)\s+in\s+(?P<place>.+)',re.IGNORECASE)

def find_places(p):
    url = 'http://api.censusreporter.org/1.0/geo/search?prefix=%s' % p
    response = requests.get(url)
    return response.json()

class SimpleCensusParser(Parser):
    def search(self, s):
        if SIMPLE_PATTERN.match(s):
            d = SIMPLE_PATTERN.match(s).groupdict()
            # figure out which table for noun
            table = "foo"
            # if we didn't get a table, we would return before making this API call...
            places = find_places(d['place'])
            return SimpleCensusMatch(table, places)

class SimpleCensusMatch(Match):
    """docstring for SimpleCensusMatch"""
    def __init__(self, table, places):
        self.table = table
        self.places = places
        # we would need to get some data
    