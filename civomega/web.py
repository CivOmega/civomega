import logging

from flask import render_template, request
from werkzeug.exceptions import NotFound

from civomega.core import app
from civomega.registry import REGISTRY

log = logging.getLogger(__name__)


@app.route("/ask")
def ask():
    q = request.args.get('question')

    search_results = []
    for parser_id in REGISTRY.parsers:
        parser = REGISTRY.parsers[parser_id]()
        search_result = parser.search(q)
        if search_result != None:
            if type(search_result) == list:
                search_results.extend(search_result)
            else:
                search_results.append(search_result)
    out = ""
    for r in search_results:
        out += "<div class='result'>%s</div>" % r.as_html()
    if len(search_results) == 0:
        out += "<div class='error'>We don't understand the question yet, but that should change eventually.</div>"

    return out



@app.route("/")
def index():
    return render_template('index.html')


if __name__ == "__main__":
    app.run(port=5000)
