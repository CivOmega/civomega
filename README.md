# CivOmega

CivOmega makes asking questions of complex data easier.  It's a simple tool for helping you map plain-text questions to the data that you have stored in your database.

## How does it work?


## How do I install it?

You’ll need [Python](http://python.org/) installed. (Python 2.7.X is
recommended. **CivOmega** has not been tested with Python 3.) Using
[pip](http://www.pip-installer.org/) and
[a virtualenv](http://www.virtualenv.org/) is also recommended (and the
following instructions assume using these packages).

1. Clone the **CivOmega** repository
  ```
  git clone https://github.com/pudo/dataomega.git civomega
  ```

2. Create a virtual environment in the `civomega` directory, change to that directory,
   and activate the newly-created virtualenv.

   ```
   virtualenv civomega
   cd civomega
   source bin/activate
   ```

3. Install dependencies
   ```
   make install
   ```

4. Run the server
   ```
   make run
   ```

## Code Overview

See `civomega/match.py` and `civomega/parser.py`. Also see
`tests/test_campaign_finance.py`, which contains example implementations of
*Parsers* and *Matchers*.

* **Parsers** - Answers a specific type of question — "How much money has
  {candidate} raised?" — with *Matches*.
* **Matches** — Connect a value — like `candidate` above — to the underlying
  dataset, returning an extraction result like `102000000`, plus the ability
  to return the result `as_html` or `as_json`.



