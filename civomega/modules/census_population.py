from civomega import Parser, Match
from jinja2 import Environment, PackageLoader
from civomega.registry import REGISTRY

env = Environment(loader=PackageLoader('civomega', 'templates'))

import re
import json
import requests
import bisect

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

SEX_AGE = { # table id B01001
    'key_ages': [
        0,
        5,
        10,
        15,
        18,
        20,
        21,
        22,
        25,
        30,
        35,
        40,
        45,
        50,
        55,
        60,
        62,
        65,
        67,
        70,
        75,
        80,
        85,
        3200,
        454656456
    ],
    'male': {
        0: "b01001003", # means 0 to 4 years old
        5: "b01001004", 
        10: "b01001005",
        15: "b01001006",
        18: "b01001007",
        20: "b01001008",
        21: "b01001009",
        22: "b01001010",
        25: "b01001011",
        30: "b01001012",
        35: "b01001013",
        40: "b01001014",
        45: "b01001015",
        50: "b01001016",
        55: "b01001017",
        60: "b01001018",
        62: "b01001019",
        65: "b01001020",
        67: "b01001021",
        70: "b01001022",
        75: "b01001023",
        80: "b01001024",
        85: "b01001049"
    },
    'female': {
        0: "b01001027", 
        5: "b01001028", 
        10: "b01001029",
        15: "b01001030",
        18: "b01001031",
        20: "b01001032",
        21: "b01001033",
        22: "b01001034",
        25: "b01001035",
        30: "b01001036",
        35: "b01001037",
        40: "b01001038",
        45: "b01001039",
        50: "b01001040",
        55: "b01001041",
        60: "b01001042",
        62: "b01001043",
        65: "b01001044",
        67: "b01001045",
        70: "b01001046",
        75: "b01001047",
        80: "b01001048",
        85: "b01001049"
    }
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

class SexAgeCensusParser(Parser):
    def search(self, s):
        if SIMPLE_PATTERN.match(s):
            d = SIMPLE_PATTERN.match(s).groupdict()
            places = find_places(d['place'])
            if places:
                noun = d['noun'].strip().lower()
                if noun == "men":
                    return SexAgeMatch(['male'], 0, 200, places)
                elif noun == "women":
                    return SexAgeMatch(['female'], 0, 200, places)
                elif noun == "people":
                    return SexAgeMatch(['male','female'], 0, 200, places)
        return None


class FieldInTableMatch(Match):
    template = None # specify in subclass
    table = None # specify in subclass
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
            'place': self.place,
            'population': self.data[self.geoid][self.field],
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


class AsianOriginMatch(FieldInTableMatch):
    template = 'census/b03001.html'
    table = 'B02006'

    def __init__(self, field, places):
        super(AsianOriginMatch,self).__init__(field, places)

class SexAgeMatch(FieldInTableMatch):
    template = 'census/b03001.html'
    table = 'B01001'

    def __init__(self, sexes, min_age, max_age,  places):
        super(SexAgeMatch, self).__init__(None, places)
        self.sexes = sexes
        self.added_fields = []
        self.min_age = min_age
        self.max_age = max_age
        self.returned_min_age = 200
        self.returned_max_age = 0

    def _context(self):
        self.total_population = 0
        for sex in self.sexes:
            for age in range(self.min_age, self.max_age):
                self._add_bucket(sex, age)
        return {
            'place': self.place,
            'population': self.total_population,
            'age_range': (self.returned_min_age, self.returned_max_age),
            'full_data': self.data[self.geoid],
            'other_places': self.other_places
        }

    def _add_bucket(self, sex, age):
        i = bisect.bisect_left(SEX_AGE['key_ages'], age)
        
        possible_min = SEX_AGE['key_ages'][i]
        possible_max = SEX_AGE['key_ages'][i+1] - 1

        if possible_min < self.returned_min_age:
            self.returned_min_age = possible_min
        if possible_max > self.returned_max_age:
            self.returned_max_age = possible_max

        x = SEX_AGE['key_ages'][i]
        if x > 85:
            x = 85

        field = SEX_AGE[sex][x]
        if field not in self.added_fields:
            self.added_fields.append(field)
            self.total_population += self.data[self.geoid][field]

        


REGISTRY.add_parser('simple_census_parser', SimpleCensusParser)
REGISTRY.add_parser('sex_age_census_parser', SexAgeCensusParser)
