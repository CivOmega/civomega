# CivOmega

[http://www.civomega.com/](http://www.civomega.com/)

CivOmega makes asking questions of complex data easier.  It's a simple tool for helping you map plain-text questions to the data that you have stored in your database.

*Word of Warning*
This code is a prototype that came out of the [Civic Media Hackday][].  There might be APIs that are documented here that are not quite finished.  With that out of the way...

[Civic Media Hackday]: http://www.eventbrite.com/event/6650197921


## 2.X branch

See "2.X branch setup" (down below) first. Otherwise, none of this
will work.

### Running the web server locally

```shell
# cd into the repo, activate the virtualenv
cd <path/to/civomega>
source bin/activate

python manage.py runserver
```

The server should then be available at
[127.0.0.1:8000](http://127.0.0.1:8000).


## 2.X branch setup

You'll need Python, pip, and virtualenv. On Mac OS X, using Homebrew to install
everything is recommended.

### Installing Homebrew & Python dependencies

```shell
# Install Homebrew. (It's safe to run this even if you do have it
# installed.)
ruby -e "$(curl -fsSL https://raw.github.com/mxcl/homebrew/go)"

# Make sure Homebrew is up to date & install the latest Python.
brew update
brew install python --with-brewed-openssl

# Check that you've got brew-installed Python 2.7.5:
which python     # should be "/usr/local/bin/python"
python --version # should be "Python 2.7.5"

# Make sure the pip & virtualenv & stuff are the latest, too:
pip install -UI setuptools pip virtualenv
```

### Check out the repo & set it up

```shell
cd <wherever_you_want_the_repo_to_go>
git clone https://github.com/mtigas/civomega.git
cd civomega

# make sure you're using this branch
git checkout 2.x

# set it up as a virtualenv -- a self-contained python
# app that doesn't affect your system or other Python-using
# projects on your computer.
virtualenv --no-site-packages .

# these settings further make sure that the CivOmega Python
# repo doesn't confuse itself or other Python projects on your
# system.
echo "export PIP_RESPECT_VIRTUALENV=true" >> bin/activate
echo "unset DJANGO_SETTINGS_MODULE" >> bin/activate

# "activate" the virtualenv
source bin/activate

# Tell pip to install Django & all the other requirements
pip install -r requirements.txt
```

### If you've already set up the repo

All you'll need to do is to `cd` into the repo and `source bin/activate`
to make it so your Python is aware of all the CivOmega commands.

If you update to a newer version in `git` and CivOmega stops working,
you might need to update your local repo dependencies to whatever
may have been updated in `requirements.txt`. To do this, make sure
you've `source bin/activate`'d your repo and then you can run the
`pip install -r requirements.txt` command again.
