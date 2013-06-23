from civomega import Parser, Match
from jinja2 import Environment, PackageLoader
from civomega.registry import REGISTRY

env = Environment(loader=PackageLoader('civomega', 'templates'))

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

SPECIFIC_ASIAN_ORIGIN = { # table id = B02006
    '02006001': 'Total:',
    '02006002': 'Asian Indian',
    '02006003': 'Bangladeshi',
    '02006004': 'Cambodian',
    '02006005': 'Chinese , except Taiwanese',
    '02006006': 'Filipino',
    '02006007': 'Hmong',
    '02006008': 'Indonesian',
    '02006009': 'Japanese',
    '02006010': 'Korean',
    '02006011': 'Laotian',
    '02006012': 'Malaysian',
    '02006013': 'Pakistani',
    '02006014': 'Sri Lankan',
    '02006015': 'Taiwanese',
    '02006016': 'Thai',
    '02006017': 'Vietnamese',
    '02006018': 'Other Asian',
    '02006019': 'Other Asian, not specified',

}

class SimpleCensusParser(Parser):
    def search(self, s):
        if SIMPLE_PATTERN.match(s):
            field = None
            d = SIMPLE_PATTERN.match(s).groupdict()
            # figure out which table for noun
            noun = d['noun'].strip()
            if noun.lower().startswith('dominican'):
                field = "b03001007"
            elif noun.lower().startswith('chile'):
                field = "b03001019"
            # if we didn't get a table, we would return before making this API call...
            if field:
                places = find_places(d['place'])
                return HispanicOriginMatch(field, places)
        return None



class HispanicOriginMatch(Match):
    template = ""
    """docstring for SimpleCensusMatch"""
    def __init__(self, field, places):
        self.table = 'B03001'
        self.field = field
        self.place = places[0]
        self.other_places = places[1:]
        self.geoid = places[0]['full_geoid']
        # we would need to get some data
        url = 'http://api.censusreporter.org/1.0/acs2011_5yr/B03001?geoids=%s' % self.geoid
        resp = requests.get(url)
        self.data = resp.json()

    def _context(self):
        return {
            'place': self.place,
            'population': self.data[self.geoid][self.field],
            'full_data': self.data[self.geoid],
            'other_places': self.other_places
        }
    def as_json(self):
        return json.dumps(self._context())

    def as_html(self):
        template = env.get_template('census/b03001.html')
        return template.render(**self._context())

REGISTRY.add_parser('simple_census_parser', SimpleCensusParser)
