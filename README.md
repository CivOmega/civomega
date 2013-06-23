# CivOmega

CivOmega makes asking questions of complex data easier.  It's a simple tool for helping you map plain-text questions to the data that you have stored in your database.

## How does it work?


## How do I install it?



## Code Overview

See `civomega/match.py` and `civomega/parser.py`. Also see
`tests/test_campaign_finance.py`, which contains example implementations of
*Parsers* and *Matchers*.

* **Parsers** - Answers a specific type of question — "How much money has
  {candidate} raised?" — with *Matches*.
* **Matches** — Connect a value — like `candidate` above — to the underlying
  dataset, returning an extraction result like `102000000`, plus the ability
  to return the result `as_html` or `as_json`.

