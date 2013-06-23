import logging

from flask import render_template, request
from werkzeug.exceptions import NotFound

from dataomega.core import app
from dataomega.registry import REGISTRY

log = logging.getLogger(__name__)


@app.route("/ask")
def ask():
    q = request.args.get('question')

    search_results = []
    for parser_id in REGISTRY.parsers:
        parser = REGISTRY.parsers[parser_id]()
        search = parser.search(q)
        if search != None:
            search_results.append(search)

    out = "<h1>%s</h1>" % q
    for r in search_results:
        out += "<div>%s</div>" % r.as_html()

    return out



@app.route("/")
def index():
    return render_template('index.html')


if __name__ == "__main__":
    app.run(port=5000)
