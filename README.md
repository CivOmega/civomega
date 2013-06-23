# CivOmega

CivOmega makes asking questions of complex data easier.  It's a simple tool for helping you map plain-text questions to the data that you have stored in your database.

*Word of Warning*
This code is a prototype that came out of the [Civic Media Hackday][].  There might be APIs that are documented here that are not quite finished.  With that out of the way...

[Civic Media Hackday]: http://www.eventbrite.com/event/6650197921


## How does it work?
CivOmega takes a question and attempts to parse it to find a match against the various data it knows about.  You create the parsers that determine if a question matches something you can provide with your data.

For example, imagine you wanted to know how much money the candidate Animated Unicorn raised.  You could search for it like this:

    import civomega
    result = civomega.search("How much much has Animated Unicorn raised?")
    result.as_json() == '{"raised": 1010000}'


So how's it all work?  You need a database, a parser that can determine if a question can be answered by a database, and the matches that can be returned.  Let's start with a *really* simple database that looks like this:

    AWESOME_DATABASE = {
        "Cartoon Rabbit": {
            "contributors": [
                ("Citizens for a Rabbit-like tomorrow!", 100000),
                ("Hopped Up Citizens", 2500000),
            ],
        },
        "Animated Unicorn": {
            "contributors": [
                ("United for Unicorns", 1000000),
                ("Citizens against Cartoon Rabbit", 10000),
            ],
        }
    }

You can see that the response you got back from your search came from adding all of the contributions to `Animated Unicorn`.  What you need to do next is parse the question to understand if there's even a possible match.


### Creating a Parser

Now that you have a simple, in-memory database setup, you need to parse the question asked to determine whether you can possibly provide a match.  Let's stick with simple and create a regular-expression parser to do a simple match.

    import re
    import civomega


    class MoneyRaisedParser(civomega.Parser):
        def __init__(self):
            pattern = r'How much money has (?P<filer>([A-Z][a-z]*\s?)+) raised'
            self.matcher = re.compile(pattern)

        def search(self, s):
            match = self.matcher.search(s)
            if match is None:
                return None
            return MoneyRaisedMatch(s, match.groupdict())

    civomega.site.register(MoneyRaisedParser)

This parser is pretty niave since it uses a simple [regular express][regex-problems], but it's a nice demo.  The `__init__` method configures the regular expression needed to do a match and `search` handles the actual matching.

You return `None` if you know you can't handle the question, otherwise you return either a Match object or a `list` of Match objects.

[regex-problems]: http://www.codinghorror.com/blog/2008/06/regular-expressions-now-you-have-two-problems.html


### Creating a Match

Once you make it this far, you have a match that might have real data associated with it.  It's up to you to figure that out via your Match object.  Here's a simple implementation that interacts with the in-memory database above:

    class MoneyRaisedMatch(Match):
        def extract(self):
            if self.data['filer'] not in AWESOME_DATABASE:
                contributors = []
            else:
                contributors = AWESOME_DATABASE[self.data['filer']]['contributors']
            self.total_money_raised = sum([a[1] for a in contributors])

        def as_html(self):
            return str(self.total_money_raised)

        def as_json(self):
            return json.dumps({"raised": self.total_money_raised})

Each `Match` object that you create needs to implement three methods:

#### `extract`
This method is called as soon as `self.search` and `self.data` are set.  `self.search` is the raw search string that the `Parser` thinks matched and `self.data` is the data it was able to extract.  In the case of your `MoneyRaisedParser` above, `self.data` is a dictionary of matching values in the regular expression.

Keep in mind this is just an example, so don't get caught up on the implementation.  In a real-world example, `extract` would talk to an API or a database to determine the amount raised instead of doing everything in memory.

#### `as_html`
This should take the extracted data (if anything) and return it as a string that can be rendered as HTML.  This can be as simple or complex as you want.  This example returns a simple string, but you could build tables, lists, or whatever you want and return it.

#### `as_json`
This returns the seralized version of the match.  Again, there's no specified standard for what the data is.


## Going beyond! (or We Need YOU!)

The example parser and matches here are pretty basic at this point.  You can go as far as you want with your parser.  Want to do natural language processing and get creative?  Go for it.  The only requirement right now is to return something other than `None` when you find a match.

But this isn't the end!  There's still a ton of work left to do and we need your help.  Here's a list of ideas that we've batted around:

* Weight and order matches
* Provide a JavaScript SDK for use outside of the demo
* Parse the search term and provide data to `search` in addition to the raw data so you can determine possible matches more easily
* Build up a library of parsers that work with open APIs


## How do I install it?

Using `pip`, you can install it by doing `pip install .` within the repository.  You can also do `pip install civomega`.
