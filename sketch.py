import json
import re

# from dataomega import site

# ## "Database"
#
# This is a very simple "database" that can be used for testing purposes
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


# think of it like x
class Matcher(object):
    def __init__(self):
        # do some setup
        pass

    def search(self, s):
        # do some sort of matching and return a Match or None
        pass


# located in dataomega.matches
class Match(object):
    def __init__(self, search, data):
        self.search = search
        self.data = data
        self.extract()  # TODO: make lazy

    @property
    def certainty(self):
        # come up with a way to say
        pass

    def as_html(self):
        pass

    def as_json(self):
        pass


class MoneyRaisedMatcher(Matcher):
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


class ContributorMatcher(Matcher):
    def __init__(self):
        pattern = r'Who (gave|gives) money to (?P<filer>([A-Z][a-z]*\s?)+)+'
        self.matcher = re.compile(pattern)

    def search(self, s):
        match = self.matcher.search(s)
        if match is None:
            return None
        return ContributorsListMatch(s, match.groupdict())


class ContributorsListMatch(Match):
    def extract(self):
        self.contributors = AWESOME_DATABASE[self.data['filer']]['contributors']

    def as_html(self):
        r = "<ul>"
        for contributor in self.contributors:
            r += "<li>%s</li>" % contributor
        return r

    def as_json(self):
        return json.dumps(self.contributors)


# site.register(ContributorMatcher)


#############
# Eventually --
# import dataomega
# matches = dataomega.search("Who gave money to Rick Perry")
#
# for now
matcher = ContributorMatcher()
print matcher.search("Who gave money to Rick Perry").as_json()
print matcher.search("Who gave money to David Dewhurst").as_json()



# or
# matches = dataomega.search("How much money has Rick Perry raised")
matcher = MoneyRaisedMatcher()
print matcher.search("How much money has Rick Perry raised").as_json()
print matcher.search("How much money has David Dewhurst raised").as_json()
#
