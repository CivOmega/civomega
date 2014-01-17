# coding=utf-8
from django.http import HttpResponse
import json

from civomega.codata.models import Module, QuestionPattern

def ask(request):
    return HttpResponse("Sorry, just a stub.", content_type="text/plain")


def _return_jsonp(data, callback):
    # "data" might be a dict (in which case we still need to JSON it)
    # or a string (assumed JSON already)
    if type(data) == dict:
        data = json.dumps(data, indent=2)

    # if callback is none, render as JSON
    # if we have a callback, render as JSONP
    if callback:
        return HttpResponse("%s(%s)" % (callback, data),
            content_type="application/json-p")
    else:
        return HttpResponse(data, content_type="application/json")


def pattern_match(request):
    query = request.GET.get('q', None)
    callback = request.GET.get('callback', None)

    # TODO actually try to narrow
    pattern_matches = []
    for m in Module.objects.all():
        for p in m.questionpattern_set.all():
            pattern_matches.append({
                'id': p.id,
                'pattern': p.pattern_str
            })

    data = {
      'q': query,
      'matches': pattern_matches
    }
    return _return_jsonp(data, callback)

def pattern_invoke(request):
    pattern_id = request.GET.get('id', None)
    callback = request.GET.get('callback', None)
    args = request.GET.get('args', '')

    # TODO:
    # * what do we want results JSON to look like
    # * we should probably actually use render_answer_json helpers, etc

    pattern = QuestionPattern.objects.get(id=pattern_id)
    answer_data = pattern.answer(args.split(','))

    data = {
      'pattern_id': pattern_id,
      'pattern_str': pattern.pattern_str,
      'module_name': pattern.module.name,
      'module_pyname': pattern.module.pymodule,
      'answer_data': answer_data
    }
    return _return_jsonp(data, callback)

def generic_query(request):
    # TODO
    query = request.GET.get('q', None)
    callback = request.GET.get('callback', None)

    data = {
      'q': query
    }
    return _return_jsonp(data, callback)
