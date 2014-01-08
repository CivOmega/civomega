# coding=utf-8
from django.http import HttpResponse
import json

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

    data = {
      'q': query,
      'matches': (
        {'id': 1, 'pattern': 'What bills are about {subject}?'}
      )
    }
    return _return_jsonp(data, callback)

def pattern_invoke(request):
    module_id = request.GET.get('id', None)
    callback = request.GET.get('callback', None)

    # TODO:
    # 1 fetch module (module_id)
    # 2 pass `request` to module
    # 3 module will pick up the key->value combinations associated
    #   with that pattern, maybe? i.e. subject = request.GET.get('subject')
    # 4 now we have args for module to do API call, return results
    # * what do we want results JSON to look like

    data = {
      'module_id': module_id
    }
    return _return_jsonp(data, callback)

def generic_query(request):
    query = request.GET.get('q', None)
    callback = request.GET.get('callback', None)

    data = {
      'q': query
    }
    return _return_jsonp(data, callback)
