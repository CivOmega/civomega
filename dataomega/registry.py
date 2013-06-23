

class MatcherRegistry(object):

    def __init__(self):
        self.matchers = {}

    def add_matcher(self, name, matcher_cls):
        self.matchers[name] = matcher

REGISTRY = MatcherRegistry()

# REGISTRY.add_matcher('census', CensusMatcher)
