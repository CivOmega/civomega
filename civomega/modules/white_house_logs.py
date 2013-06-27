from civomega import Parser, Match
from jinja2 import Environment, PackageLoader
from civomega.registry import REGISTRY

env = Environment(loader=PackageLoader('civomega', 'templates'))

import re
import json
import requests
import string
import datetime

# Who visit(s/ed) the White House?
SIMPLE_PATTERN = re.compile('^\s*who\svisit(?:ed|s)\sthe\swhite\shouse', re.IGNORECASE)

# necessary because datetime doesn't support non-zero padded numbers in strptime
DATE_PATTERN = re.compile("(?P<month>\d*)/(?P<day>\d*)/(?P<year>\d*) (?P<hour>\d*):(?P<minute>\d*)")

API_ENDPOINT = 'http://explore.data.gov/resource/644b-gaut.json?'

# (When/how many times/why/who) did <name> visit (at|in) the White House?
VISITOR_PATTERN = re.compile('^\s*(?:when|how\smany\stimes|why|who|has|)\s*(?:did|was|has|)\s*(?P<names>(\s?\w+)+)\s(?:visited|visit|visiting|been\sto)\s*(?:at|in|)\sthe\swhite\shouse', re.IGNORECASE)

# TODO: Who visit(ed/s) Rahm Emanual at the White House?


class SimpleWhiteHouseLogSearchParser(Parser):
    def search(self, s):
        # filters for keywords before breaking out the regex brass knuckles
        if s.lower().find('white house') != -1 and SIMPLE_PATTERN.match(s):
            return SimpleWhiteHouseLogSearchMatch()
        return None


class VisitorWhiteHouseLogSearchParser(Parser):
    def search(self, s):
        # filters for keywords before breaking out the regex brass knuckles
        if s.lower().find('white house') != -1:
            m = VISITOR_PATTERN.match(s)
            if m:
                d = m.groupdict()
                # figure out which table for noun
                names = d['names'].strip().split()
                return VisitorWhiteHouseLogSearchMatch(names)
        return None


class SimpleWhiteHouseLogSearchMatch(Match):

    """docstring for SimpleWhiteHouseLogSearchMatch"""
    def __init__(self):
        url = API_ENDPOINT + '$limit=25&$order=release_date%20DESC'
        resp = requests.get(url)
        self.data = {'name': '', 'results': resp.json()}

    def format_data(self, data):
        for item in data['results']:
            item['visitor_name'] = string.capwords(item.get('namefirst', ''))
            item['visitor_name'] += " " + string.capwords(item.get('namelast', ''))
            item['visited_name'] = string.capwords(item.get('visitee_namefirst', ''))
            if string.capwords(item.get('visitee_namelast', '')) != 'And':
                item['visited_name'] += " " + string.capwords(item.get('visitee_namelast', ''))
            if item['visited_name'].rstrip().lstrip() == 'Potus':
                item['visited_name'] = 'The President'
            item['description'] = item.get('description', '').lower()

            led = item.get('lastentrydate', '')
            dd = DATE_PATTERN.match(led)
            if dd:
                dd = dd.groupdict()
                year = int(dd['year'])
                # yes, this is how I'm doing this
                if year < 2000:
                    year += 2000
                dt = datetime.datetime(year, int(dd['month']), int(dd['day']), int(dd['hour']), int(dd['minute']))

                # will fail on systems with non-GNU C libs (i.e. Windows) due to %- removal of zero-padding
                item['lastentry_date'] = dt.strftime('%-m/%-d/%Y %-I:%M%p')
            else:
                item['lastentry_date'] = led

        return data

    def as_json(self):
        return json.dumps(self.data)

    def as_html(self):
        template = env.get_template('white_house_logs/simple_search.html')
        return template.render(**self.format_data(self.data))


class VisitorWhiteHouseLogSearchMatch(SimpleWhiteHouseLogSearchMatch):

    """docstring for VisitorWhiteHouseLogSearchMatch"""
    def __init__(self, names):
        firstname = names[0][0].capitalize() + names[0][1:]
        lastname = names[-1][0].capitalize() + names[-1][1:]

        #print(firstname + " " + lastname)

        url = API_ENDPOINT
        if firstname.strip() != '':
            url += 'namefirst=%s&' % (firstname)
        if lastname.strip() != '':
            url += 'namelast=%s&' % (lastname)
        url += '$limit=25&$order=release_date%20DESC'

        resp = requests.get(url)
        self.data = {'name': (firstname + " " + lastname).lstrip(), 'results': resp.json()}

REGISTRY.add_parser('simple_white_house_log_search', SimpleWhiteHouseLogSearchParser)
REGISTRY.add_parser('visitor_white_house_log_search', VisitorWhiteHouseLogSearchParser)
