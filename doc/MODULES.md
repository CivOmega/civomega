## Creating a Module
CivOmega Modules are what connect datasets and APIs to question patterns.  To create a new module, follow the instructions below.  If you're actually interested in adding more questions to a dataset that already exists, we suggest that you contribute to an existing module instead of creating a new one from the ground up.

Modules have the following components:

- [parsers.py](comod_example/parser.py) - this is where you define question routes and answer logic
- [patterns.py](comod_example/patterns.py) - this is where you define the list of question patterns that your module knows how to answer
- [templates](comod_example/templates) - this is where you define the output format for your answers

### Step 1: Fork, Clone, and Configure

To build a module you first need to create a working version of [CivOmega](https://github.com/CivOmega/civomega) set up on your development environment.  Once this is done:

* Fork the [CivOmega Module Bootstrap](https://github.com/CivOmega/civomega-mod-bootstrap) repository in GitHub. (It's the big button in the upper-right of the page.)
* In your GitHub fork, go to the settings and rename it from `civomega-mod-bootstrap` to `civomega-mod-meaningful-name` (or whatever you'd like to call your module)
* Clone your fork alongside wherever you cloned CivOmega. (If you have `civomega` checked out as `$HOME/Projects/civomega`, clone it from `$HOME/Projects` so you end up with `$HOME/Projects/civomega-mod-meaningful-name` or etc.)

**Inside the repo:**

* Edit `setup.py` and in the `setup(name=` portion, change `civomega-mod-bootstrap` to `civomega-mod-meaningful-name` (or whatever your module is called)
* Rename the `comod_bootstrap` directory to `comod_meaningful_name` (*note*: you must use underscores in the directory name).
* Inside *that* directory, there's a `templates` directory. Inside there, rename the `comod_bootstrap` directory as well (using the same name as before, with underscores).

**Inside your `civomega` repo:**

* Update `CIVOMEGA_MODULES` in `civomega/settings.py` to include your module (using underscores like the directory name, i.e. `comod_meaningful_name`). It should look like this:

    ```python
    CIVOMEGA_MODULES = (
        'comod_example',
        'comod_sunlightbills',
        'comod_meaningful_name',
    )
    ```

* Update `bin/activate` to include this line at the bottom, swapping out `$HOME/Projects/civomega-mod-meaningful-name` with the full path to where you cloned the repo:

    ```bash
    export PYTHONPATH="$HOME/Projects/civomega-mod-meaningful-name:$PYTHONPATH"
    ```

...And make sure you open a new terminal, `cd` to the `civomega` directory, and `source bin/activate` to make the changes take effect.

You can now run CivOmega, and it will pick up changes as you make them in your `civomega-mod-meaningful-name` repo.

### Step 2: Define Patterns

In `comod_example/patterns.py` you must define `PATTERNS` to contain a list of question patterns (strings) that your module knows how to answer.  These patterns should have "blanks" which will allow users to enter the types of things they are looking for.

Wrap "blanks" in {braces}, and keep in mind that the content inside the braces dictate the type of object being entered.  This content should be lowercase, underscore_separated.

For example:

```python
PATTERNS = frozenset([
    "how much money did {organization} donate in {year}",
    "is {person} a {thing}?",
    "is {person} a {thing} in {place}?",
])
```

The blanks must be unique inside the pattern. You can't have `"what bills did {person} and {person} sponsor?"`, but you should do something like this instead: `"what bills did {person_1} and {person_2} sponsor?"`

You can create multiple categories of pattern as well, if your module knows how to answer more than one type of question.  See the [Sunlight bill module](https://github.com/CivOmega/civomega-mod-sunlightbills) for an example of this type of behavior.

### Step 2a: Updating the Pattern Database

**Important**: Every time you edit patterns, you will have to refresh CivOmega's known pattern list.  When you're ready to test your module, you will need to run:

```shell
# run these CivOmega commands from the `civomega` directory, after you've done `source bin/activate`
python manage.py update_patterns
python manage.py runserver
```

### Step 3: Parsing Question Input

`parsers.py`: `answer_pattern(pattern, args)`, `render_answer_html(answer_data)`, `render_answer_json(answer_data)` are required, but you can define more functions as you need them.


#### Understanding `answer_pattern`
When a user uses the CivOmega interface to fill in the blanks of one of your module's patterns, your module will be invoked by calling your answer_pattern method.  The `pattern` parameter will contain the pattern that was used, while the `args` will contain an ordered list of the the arguments supplied.

See the [Sunlight Mod Example](https://github.com/CivOmega/civomega-mod-sunlightbills) for an example of how to map parameters to their associated keys.

Whatever this method returns will be passed to the render_answer_html and render_answer_json method as data.  The return value should always be an object of the structure:

```python
{
    type: '',
    data: {}
}
```


#### Using Python Libraries
If you need to use other Python libraries inside your module you can add them to `setup.py`, under `install_requires`. For example, if you want to use [requests](http://docs.python-requests.org/en/latest/) to help you use an HTTP API, you can do the following in `setup.py`. (Again, the [Sunlight bill module](https://github.com/CivOmega/civomega-mod-sunlightbills) has an example of this.)

```python
      install_requires=[
          'requests',
      ],
```

Because you've set up `civomega` to run your module "live" from the code directory you're editing (instead of installing it from the internet), you'll have to `pip install requests` (or whatever library you wanted to add) -- as long as you're in a terminal that you've "activated" (i.e. you've done `source bin/activate` in the `civomega` directory first).

### Step 4: Rendering ourput

[TODO]

HTML files in `comod_example/templates/comod_example/`