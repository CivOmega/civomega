import json
import re

from civomega.match import Match
from civomega.parser import Parser

from civomega.registry import REGISTRY


# dumb example, flat database of campaign contributions in one year
AWESOME_DATABASE = {
    "Rick Perry": {
        "contributors": [
            ("Texans for Perry", 1238458),
            ("Texans who are really for Perry", 1584830),
            ("Americans for Other Stuff", 500)
        ],
        "total_money_raised": 1238458+1584830+500 # just here as a sanity check
    },
    "David Dewhurst": {
        "contributors": [
            ("Texans for Dewhurst", 58383),
            ("Texans who are really for Dewhurst", 2831284)
        ],
        "total_money_raised": 58383+2831284 # just here as a sanity check
    }
}


class MoneyRaisedParser(Parser):
    def __init__(self):
        pattern = r'How much money has (?P<filer>([A-Z][a-z]*\s?)+) raised'
        self.matcher = re.compile(pattern)

    def search(self, s):
        match = self.matcher.search(s)
        if match is None:
            return None
        return MoneyRaisedMatch(s, match.groupdict())



class MoneyRaisedMatch(Match):
    def extract(self):
        contributors = AWESOME_DATABASE[self.data['filer']]['contributors']
        self.total_money_raised = sum(map(lambda x: x[1], contributors))

    def as_html(self):
        return str(self.total_money_raised)

    def as_json(self):
        return json.dumps({"raised": self.total_money_raised})


class ContributorParser(Parser):
    def __init__(self):
        pattern = r'Who (gave|gives) money to (?P<filer>([A-Z][a-z]*\s?)+)+'
        self.matcher = re.compile(pattern)

    def search(self, s):
        match = self.matcher.search(s)
        if match is None:
            return None
        return ContributorsListMatch(s, match.groupdict())



class ContributorsListMatch(Match):
    def __init__(self, *args, **kwargs):
        self.contributors = False
        super(ContributorsListMatch, self).__init__(*args, **kwargs)

    def extract(self):
        if self.data['filer'] in AWESOME_DATABASE:
            contributors = AWESOME_DATABASE[self.data['filer']]['contributors']
            self.contributors = map(lambda x: x[0], contributors)

    def as_html(self):
        if not self.contributors:
            return None

        r = "<ul>"
        for contributor in self.contributors:
            r += "<li>%s</li>" % contributor
        r += "</ul>"
        return r

    def as_json(self):
        return json.dumps(self.contributors) if self.contributors else None




REGISTRY.add_parser('money_raised', MoneyRaisedParser)
REGISTRY.add_parser('contributors', ContributorParser)
