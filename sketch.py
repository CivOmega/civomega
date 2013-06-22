import re

from dataomega import site


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
        return json.dumps(self.data)


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
        filer = Filer.objects.get(name=self.data['filer'])
        self.contributors = Contributors.objects.filter(filer=filer)


site.register(ContributorMatcher)


#############
import dataomega
matches = dataomega.search("Who gave money to Rick Perry")
best_match = matches[0]
best_match.contributors



# or
matches = dataomega.search("How much money has Rick Perry raised")

for match in matches:
    #
