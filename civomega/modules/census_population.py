from civomega import Parser, Match
from jinja2 import Environment, PackageLoader
from civomega.registry import REGISTRY

env = Environment(loader=PackageLoader('civomega', 'templates'))

import re
import json
import requests

SIMPLE_PATTERN = re.compile('^\s*(?:how many|how much|which are|which)(?P<noun>.+?)\s+(?:live in|are in|in)\s+(?P<place>[\w\s]+)\??',re.IGNORECASE)

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
    'b02006001': 'Total:',
    'b02006002': 'Asian Indian',
    'b02006003': 'Bangladeshi',
    'b02006004': 'Cambodian',
    'b02006005': 'Chinese , except Taiwanese',
    'b02006006': 'Filipino',
    'b02006007': 'Hmong',
    'b02006008': 'Indonesian',
    'b02006009': 'Japanese',
    'b02006010': 'Korean',
    'b02006011': 'Laotian',
    'b02006012': 'Malaysian',
    'b02006013': 'Pakistani',
    'b02006014': 'Sri Lankan',
    'b02006015': 'Taiwanese',
    'b02006016': 'Thai',
    'b02006017': 'Vietnamese',
    'b02006018': 'Other Asian',
    'b02006019': 'Other Asian, not specified',

}


class SimpleCensusParser(Parser):
    def search(self, s):
        if SIMPLE_PATTERN.match(s):
            d = SIMPLE_PATTERN.match(s).groupdict()
            places = find_places(d['place'])
            if places:
            # figure out which table for noun
                noun = d['noun'].strip().lower()
                if noun[-1] == 's': noun = noun[:-1]
                for field,name in SPECIFIC_HISPANIC_ORIGIN.items():
                    if name.lower().startswith(noun):
                        return HispanicOriginMatch(field, places)
                for field,name in SPECIFIC_ASIAN_ORIGIN.items():
                    if name.lower().startswith(noun):
                        return AsianOriginMatch(field, places)
        return None



class FieldInTableMatch(Match):
    template = None # specify in subclass
    table = None # specify in subclass
    label = None # evaluate in subclass, e.g. "Dominican", "Chinese"
    def __init__(self, field, places):
        self.field = field
        self.place = places[0]
        self.other_places = places[1:]
        self.geoid = places[0]['full_geoid']
        self.load_table_data()
        
    def load_table_data(self):
        # we would need to get some data
        url = 'http://api.censusreporter.org/1.0/acs2011_5yr/%s?geoids=%s' % (self.table,self.geoid)
        resp = requests.get(url)
        self.data = resp.json()

    def _context(self):
        return {
            'label': self.label,
            'place': self.place,
            'population': int(self.data[self.geoid][self.field]),
            'full_data': self.data[self.geoid],
            'other_places': self.other_places
        }

    def as_json(self):
        return json.dumps(self._context())

    def as_html(self):
        return env.get_template(self.template).render(**self._context())

        
class HispanicOriginMatch(FieldInTableMatch):
    template = 'census/b03001.html'
    table = 'B03001'

    def __init__(self, field, places):
        super(HispanicOriginMatch,self).__init__(field, places)
        self.label = SPECIFIC_HISPANIC_ORIGIN[self.field]

    def _context(self):
        d = super(HispanicOriginMatch,self)._context()
        d['field_labels'] = SPECIFIC_HISPANIC_ORIGIN
        return d
        
class AsianOriginMatch(FieldInTableMatch):
    template = 'census/b02006.html'
    table = 'B02006'

    def __init__(self, field, places):
        super(AsianOriginMatch,self).__init__(field, places)
        self.label = SPECIFIC_ASIAN_ORIGIN[self.field]


REGISTRY.add_parser('simple_census_parser', SimpleCensusParser)
