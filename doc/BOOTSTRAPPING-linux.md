# Running an instance of CivOmega

## Local OS X

### First-time setup

You'll need a basic Python environment and the ability to check out this
code repository, so you'll need at least the following packages to run CivOmega:

* **git**
* **python** (specifically **python2**)

Depending on your OS distribution of Python, you may need to manually install
[setuptools](https://pypi.python.org/pypi/setuptools). See that page for info.

Then install `pip` to facilitate the rest of the dependency installation
process:

`sudo easy_install pip`

(If your distribution uses Python 3 by default, you *may* need to change
`easy_install` to `easy_install-2.7`.)

Now install some Python tools that will help you bootstrap your CivOmega
Python environment.

```shell
sudo pip install -UI setuptools pip virtualenv
```

Pick a place to store the repo. I usually put projects in a `Code` directory
in my home folder, but you can adjust this accordingly. `cd` into that
directory. (i.e. `cd ~/Code`) Then:

```shell
git clone https://github.com/CivOmega/civomega.git
virtualenv civomega
```

(If your distribution uses Python 3 by default, you'll need to change the
`virtualenv` line to be `virtualenv -p /usr/bin/python2 civomega` or something
along those lines.)

Now we'll `cd` into the civomega repo and "activate" this environment.
Then, using `pip`, we'll install all the Python libraries defined in the
`requirements.txt` file. (This is sort of like a Ruby `Gemfile`.)

```shell
cd civomega
source bin/activate
pip install -r requirements.txt
```

You can ensure that the virtual environment is using an isolated version
of Python 2:

```shell
`which python`
python --version
```

Now you'll be able to use the Django tools to set up and use a database.
For local installations, CivOmega is configured to use a dummy `sqlite3`
database by default. You can initialize the database by doing:

```shell
python manage.py syncdb --migrate --noinput
```

From here, you should be able to run the local server by running the following
command…

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
