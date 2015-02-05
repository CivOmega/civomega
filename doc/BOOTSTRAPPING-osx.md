# Running an instance of CivOmega

## Local OS X

### First-time setup

**Install Homebrew if you don't have it**

Homebrew needs some tools from Xcode.
Install the Xcode compilers if you don't have a real copy of the
[Xcode app](https://itunes.apple.com/us/app/xcode/id497799835). If you do
have Xcode, then skip ths command.

```shell
xcode-select --install
```

Install [Homebrew](http://brew.sh/). (It's safe to run the following command
even if you do have brew installed, it'll just warn you about it. Don't do the
"reinstall" step if you do get that warning.)

```shell
ruby -e "$(curl -fsSL https://raw.github.com/Homebrew/homebrew/go/install)"
```

**Set up an up-to-date Python environment, using Homebrew**

Make sure Homebrew is up to date (so it knows about the latest software
packages) and then install Python. It will take a while to build Python.

```shell
brew update
brew install python --with-brewed-openssl
```

(If you get a `Error: python-2.X.X already installed` of some sort, do 
`brew upgrade python --with-brewed-openssl` instead of
`brew install python --with-brewed-openssl`.)

Now install some Python tools that will help you bootstrap your CivOmega
Python environment. (You may need to `sudo` this command.)

```shell
/usr/local/bin/pip install -UI setuptools pip virtualenv
```

**Download and initialize a CivOmega instance**

Pick a place to store the CivOmega code. I usually put projects in a `Code` directory
in my home folder, but you can adjust this accordingly. `cd` into that
directory.

```shell
git clone https://github.com/CivOmega/civomega.git  # check out repo
virtualenv civomega  # make a` "virtual environment"
```

A Python virtual environment basically keeps an isolated set of Python
libraries that don't interfere with your system's stuff.

Now we'll `cd` into the civomega repo and "activate" this environment.
Then, using `pip`, we'll install all the Python libraries defined in the
`requirements.txt` file. (This is sort of like a Ruby `Gemfile`.)

```shell
cd civomega
source bin/activate
pip install -r requirements.txt
```

Now you'll be able to use the Django tools to set up and use a database.
For local installations, CivOmega is configured to use a dummy `sqlite3`
database by default. You can initialize the database by doing:

```shell
python manage.py syncdb --migrate --noinput
python manage.py update_patterns
```

From here, you should be able to run the local server.

```shell
python manage.py runserver
```

…and opening your web browser to `http://127.0.0.1:8000/`.

### Running the server normally

How to do the server stuff, after the first time around.

```shell
cd civomega
source bin/activate
python manage.py runserver
```

If someone's made an update to the `requirements.txt`, do the `cd` and `source`
commands and then `pip install -r requirements.txt`.

If someone's made an update to a `models.py` file that requires a database
change, simply do a `python manage.py syncdb --migrate --noinput` once again.

### API keys

The default modules include one which queries the [Sunlight Foundation](http://sunlightfoundation.com)'s
APIs. So you'll need to have [an API key](http://sunlightfoundation.com/api/)
if you want to use that one.

Once you have the API key, make sure you do this…

```shell
export SUNLIGHT_API_KEY=$YOUR_KEY_HERE
```

…before you run `python manage.py runserver`.

(TODO: Better way to handle this. Make module disable itself at runtime if key is missing.)

### When installing new modules...

When you edit a module's code, you'll want to run `python manage.py update_patterns`
again so that the database knows about any new question/answer patterns your
code has. (If you don't do this, your module probably won't show up when you
type in a question in the CivOmega web interface!)
