from civomega import Parser, Match
from civomega.registry import REGISTRY
from django.template import loader, Context

import os
import re
import json
import requests

SIMPLE_PATTERN = re.compile('^\s*(?:who|which (legislators|people))\s(?:talk(s?)|ta|(is|are)\stalking\sabout|mention(s?))\s(?P<noun>.+)',re.IGNORECASE)

class SimpleCapitolWordsParser(Parser):
    def search(self, s):
        if SIMPLE_PATTERN.match(s):
            d = SIMPLE_PATTERN.match(s).groupdict()
            # figure out which table for noun
            noun = d['noun'].strip()
            if(noun[-1] == '?'):
                noun = noun[0:-1]
            return SimpleCapitolWordsMatch(noun)
        return None

class SimpleCapitolWordsMatch(Match):
    def __init__(self, noun):
        # we would need to get some data
        url = 'http://capitolwords.org/api/1/phrases/legislator.json?phrase=%s&sort=count&apikey=%s' % (noun, os.environ['SUNLIGHT_API_KEY'])
        resp = requests.get(url)
        self.data = resp.json()
        for r in self.data['results']:
            url = 'http://congress.api.sunlightfoundation.com/legislators?bioguide_id=%s&apikey=%s' % (r['legislator'], os.environ['SUNLIGHT_API_KEY'])
            resp = requests.get(url)
            subdata = resp.json()
            legislator_data = subdata['results']
            if legislator_data:
                r['legislator'] = legislator_data[0]['first_name'] + " " + legislator_data[0]['last_name']
            else:
                r['legislator'] = "<span class='notfound'>Name not found</span>"


    def as_json(self):
        return json.dumps(self.data)

    def as_html(self):
        template = loader.get_template('capitol_words/simple_search.html')
        return template.render(Context(self.data))

REGISTRY.add_parser('capitol_words_search', SimpleCapitolWordsParser)
