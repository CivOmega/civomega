import json


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
