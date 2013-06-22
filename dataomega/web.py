import logging

from flask import render_template
from werkzeug.exceptions import NotFound

from dataomega.core import app

log = logging.getLogger(__name__)


@app.route("/")
def index():
    return render_template('index.html')


if __name__ == "__main__":
    app.run(port=5000)
