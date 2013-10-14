from django.conf import settings

class ParserRegistry(object):

    def __init__(self):
        self.parsers = {}

    def add_parser(self, name, parser_cls):
        self.parsers[name] = parser_cls

    def __iter__(self):
        return self.parsers.values()


REGISTRY = ParserRegistry()

# REGISTRY.add_parser('census', CensusParser)


# TODO:
#if settings.get('CIVOMEGA_MODULES', None):
#  ...for module in settings.CIVOMEGA_MODULES
#     ...some sort of import magic
#     ...module.autoregister(REGISTRY)
