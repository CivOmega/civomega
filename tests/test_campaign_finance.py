import json
import re
import unittest

from dataomega.match import Match
from dataomega.parser import Parser


AWESOME_DATABASE = {
    "Rick Perry": {
        "contributors": [
            "Texans for Perry",
            "Texans who are really for Perry",
        ],
        "money": "Bazillion",
    },
    "David Dewhurst": {
        "contributors": [
            "Texans for Dewhurst",
            "Texans who are really for Dewhurst",
        ],
        "money": "Gajillion",
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
        self.money = AWESOME_DATABASE[self.data['filer']]['money']

    def as_json(self):
        return json.dumps({"raised": self.money})


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
            filer = AWESOME_DATABASE[self.data['filer']]
            self.contributors = filer['contributors']

    def as_html(self):
        if not self.contributors:
            return None

        r = "<ul>"
        for contributor in self.contributors:
            r += "<li>%s</li>" % contributor
        r += "</ul>"
        return r

    def as_json(self):
        print self.contributors
        return json.dumps(self.contributors) if self.contributors else None


class TestContributorParser(unittest.TestCase):
    def setUp(self):
        self.matcher = ContributorParser()

    def test_can_find_contributors_for_perry(self):
        result = self.matcher.search("Who gave money to Rick Perry")
        data = result.as_json()
        self.assert_("Texans for Perry" in json.loads(data))
        self.assert_("Texans who are really for Perry" in json.loads(data))

    def test_can_find_contributors_for_dewhurst(self):
        result = self.matcher.search("Who gave money to David Dewhurst")
        data = result.as_json()
        self.assert_("Texans for Dewhurst" in json.loads(data))
        self.assert_("Texans who are really for Dewhurst" in json.loads(data))

    def test_returns_none_for_nothing(self):
        result = self.matcher.search("Who did not give money to Rick Perry")
        self.assert_(result is None)


class TestMoneyRaisedParser(unittest.TestCase):
    def setUp(self):
        self.matcher = MoneyRaisedParser()

    def test_can_find_money_raised_for_perry(self):
        result = self.matcher.search("How much money has Rick Perry raised")
        data = json.loads(result.as_json())
        self.assert_(AWESOME_DATABASE['Rick Perry']['money'] == data["raised"])

    def test_can_find_money_raised_for_dewhurst(self):
        result = self.matcher.search("How much money has David Dewhurst raised")
        data = json.loads(result.as_json())
        self.assert_(AWESOME_DATABASE['David Dewhurst']['money'] == data["raised"])

    def test_returns_none_for_no_match(self):
        result = self.matcher.search("How much money didn't Rick Perry raise")
        self.assert_(result is None)
