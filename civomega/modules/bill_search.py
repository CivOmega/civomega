from civomega import Parser, Match
from civomega.registry import REGISTRY
from django.template import loader, Context

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

SUPPORT_PATTERN = re.compile('^\s*(?:what|which)\s(?:legislative\s)?(?:laws|legislation|bill(s?))\s(?:do|did|has|does)\s(?P<names>(\s?\w+)+)\s(?:sponsor|support)',re.IGNORECASE)

class SupportBillSearchParser(Parser):
    def search(self, s):
        if SUPPORT_PATTERN.match(s):
            d = SUPPORT_PATTERN.match(s).groupdict()
            # figure out which table for noun
            names = d['names'].strip().split()
            return SupportedBillSearchMatch(names)
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
        template = loader.get_template('bill_search/simple_search.html')
        return template.render(Context(self.data))

class SupportedBillSearchMatch(Match):

    """docstring for SimpleBillSearchMatch"""
    def __init__(self, names):
        # Find the legislator
        url = 'http://congress.api.sunlightfoundation.com/legislators?apikey=%s&first_name=%s&last_name=%s' % (os.environ['SUNLIGHT_API_KEY'], names[0][0].capitalize() + names[0][1:], names[-1][0].capitalize() + names[-1][1:])
        resp = requests.get(url)
        data = resp.json()
        print names[-1].capitalize()
        if(len(data['results']) == 0):
            url = 'http://congress.api.sunlightfoundation.com/legislators?apikey=%s&nickname=%s&last_name=%s' % (os.environ['SUNLIGHT_API_KEY'], names[0][0].capitalize() + names[0][1:], names[-1][0].capitalize() + names[-1][1:])
            resp = requests.get(url)
            data = resp.json()
        if(len(data['results']) == 0):
            url = 'http://congress.api.sunlightfoundation.com/legislators?apikey=%s&last_name=%s' % (os.environ['SUNLIGHT_API_KEY'], names[-1][0].capitalize() + names[-1][1:])
            resp = requests.get(url)
            data = resp.json()

        if(len(data['results']) == 0):
            self.data = {'results': []}
        else:
            bio_id = data['results'][0]['bioguide_id']
            url = 'http://congress.api.sunlightfoundation.com/bills?apikey=%s&sponsor_id=%s' % (os.environ['SUNLIGHT_API_KEY'], bio_id)
            resp = requests.get(url)
            self.data = resp.json()

    def as_json(self):
        return json.dumps(self.data)

    def as_html(self):
        template = loader.get_template('bill_search/simple_search.html')
        return template.render(Context(self.data))

REGISTRY.add_parser('simple_bill_search', SimpleBillSearchParser)
REGISTRY.add_parser('supported_bill_search', SupportBillSearchParser)
