

class MatcherRegistry(object):

    def __init__(self):
        self.matchers = {}

    def add_matcher(self, name, matcher_cls):
        self.matchers[name] = matcher

    def __iter__(self):
        return self.matchers.values()


REGISTRY = MatcherRegistry()

# REGISTRY.add_matcher('census', CensusMatcher)
