class Match(object):
    def __init__(self, search, data):
        self.search = search
        self.data = data
        self.extract()  # TODO: make lazy

    @property
    def certainty(self):
        # come up with a way to say
        raise NotImplementedError()

    def as_html(self):
        raise NotImplementedError()

    def as_json(self):
        raise NotImplementedError()
