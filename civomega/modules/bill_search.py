from civomega import Parser, Match
from jinja2 import Environment, PackageLoader
from civomega.registry import REGISTRY

env = Environment(loader=PackageLoader('civomega', 'templates'))

import os
import re
import json
import requests

SIMPLE_PATTERN = re.compile('^\s*(?:what|which)\s(?:legislative\s)?(?:laws|legislation|bill(s?))\s(?:is|was|are|were)\sabout\s(?P<noun>.+)',re.IGNORECASE)

class SimpleBillSearchParser(Parser):
    def search(self, s):
        if SIMPLE_PATTERN.match(s):
            d = SIMPLE_PATTERN.match(s).groupdict()
            # figure out which table for noun
            noun = d['noun'].strip()
            if(noun[-1] == '?'):
                noun = noun[0:-1]
            return SimpleBillSearchMatch(noun)
        return None



class SimpleBillSearchMatch(Match):

    """docstring for SimpleBillSearchMatch"""
    def __init__(self, noun):
        # we would need to get some data
        url = 'http://congress.api.sunlightfoundation.com/bills?apikey=%s&query=%s' % (os.environ['SUNLIGHT_API_KEY'], noun)
        resp = requests.get(url)
        self.data = resp.json()

    def as_json(self):
        return json.dumps(self.data)

    def as_html(self):
        template = env.get_template('bill_search/simple_search.html')
        return template.render(**self.data)

REGISTRY.add_parser('simple_bill_search', SimpleBillSearchParser)
