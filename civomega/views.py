# coding=utf-8
# import hack
#   -> import these so REGISTRY happens (i.e.
#      all these modules get loaded & activated)
#
# TODO: make this not hackish as hell, since we
#       actually have the registry & registry.add_parser
#       parts. just need to make the flexible parts flexible.
from civomega.modules import census_population
from civomega.modules import bill_search
from civomega.modules import capitol_words
from civomega.modules import white_house_logs
from civomega.modules import werewolf
# /import hack

import logging
import datetime
from django.http import HttpResponse
from django.shortcuts import render

from civomega.registry import REGISTRY

log = logging.getLogger(__name__)


def index(request):
    return render(request, 'index.html')


def ask(request):
    # pull out ?question=... part of URL
    q = request.GET.get('question')

    search_results = []
    for parser_id in REGISTRY.parsers:
        parser = REGISTRY.parsers[parser_id]()
        search_result = parser.search(q)
        print parser, search_result
        if search_result != None:
            if type(search_result) == list:
                search_results.extend(search_result)
            else:
                search_results.append(search_result)
    out = ""
    for r in search_results:
        out += "<div class='result'>%s</div>" % r.as_html()
    if len(search_results) == 0:
        out += "<div class='result'>We don't understand this kind of question yet, but that should change eventually.</div>"

    return HttpResponse(out)
