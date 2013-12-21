# coding=utf-8
from django.http import HttpResponse

def ask(request):
    return HttpResponse("Sorry, just a stub.", content_type="text/plain")
