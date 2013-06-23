from dataomega import Parser, Match

import re
import json
import requests

SIMPLE_PATTERN = re.compile('^\s*(?:how many|how much|which are|which)(?P<noun>.+)\s+in\s+(?P<place>[\w\s]+)\??',re.IGNORECASE)

def find_places(p):
    url = 'http://api.censusreporter.org/1.0/geo/search?prefix=%s' % p
    response = requests.get(url)
    return response.json()

SPECIFIC_HISPANIC_ORIGIN = { # table ID B03001
	'b03001001': 'Total:',
	'b03001002': 'Not Hispanic or Latino',
	'b03001003': 'Hispanic or Latino', # cumulative
	'b03001004': 'Mexican',
	'b03001005': 'Puerto Rican',
	'b03001006': 'Cuban',
	'b03001007': 'Dominican (Dominican Republic)',
	'b03001008': 'Central American:',
	'b03001009': 'Costa Rican',
	'b03001010': 'Guatemalan',
	'b03001011': 'Honduran',
	'b03001012': 'Nicaraguan',
	'b03001013': 'Panamanian',
	'b03001014': 'Salvadoran',
	'b03001015': 'Other Central American',
	'b03001016': 'South American', # cumulative
	'b03001017': 'Argentinean',
	'b03001018': 'Bolivian',
	'b03001019': 'Chilean',
	'b03001020': 'Colombian',
	'b03001021': 'Ecuadorian',
	'b03001022': 'Paraguayan',
	'b03001023': 'Peruvian',
	'b03001024': 'Uruguayan',
	'b03001025': 'Venezuelan',
	'b03001026': 'Other South American',
	'b03001027': 'Other Hispanic or Latino', # cumulative
	'b03001028': 'Spaniard',
	'b03001029': 'Spanish',
	'b03001030': 'Spanish American',
	'b03001031': 'All other Hispanic or Latino',
}

class SimpleCensusParser(Parser):
    def search(self, s):
        if SIMPLE_PATTERN.match(s):
            field = None
            d = SIMPLE_PATTERN.match(s).groupdict()
            # figure out which table for noun
            noun = d['noun'].strip()
            if noun.lower().startswith('dominican'):
                field = "B03001007"
            elif noun.lower().startswith('chile'):
                field = "B03001019"
            # if we didn't get a table, we would return before making this API call...
            if field:
                places = find_places(d['place'])
                return HispanicOriginMatch(field, places)
        return None

class HispanicOriginMatch(Match):
    """docstring for SimpleCensusMatch"""
    def __init__(self, field, places):
        self.table = 'B03001'
        self.field = field
        self.places = places
        self.geoid = places[0]['full_geoid']
        # we would need to get some data
        url = 'http://api.censusreporter.org/1.0/acs2011_5yr/B03001?geoids=%s' % self.geoid
        resp = requests.get(url)
        self.data = resp.json()
        
    def as_json(self):
        d = {
            'population': self.data[self.geoid][self.field],
            'full_data': self.data,
            'other_places': self.places[1:]
        }
        return json.dumps(d)
        
    def as_html(self):
        pass
    