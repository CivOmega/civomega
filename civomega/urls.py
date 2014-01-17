from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

urlpatterns = patterns('',
    url(r'^$', TemplateView.as_view(template_name="index.html"), name='homepage'),
    url(r'^ask$', 'civomega.codata.views.ask', name='ask'),

    url(r'^endpoints/pattern-match$', 'civomega.codata.views.pattern_match',
        name='pattern-match'),
    url(r'^endpoints/invoke$', 'civomega.codata.views.pattern_invoke',
        name='pattern-invoke'),
    url(r'^endpoints/generic$', 'civomega.codata.views.generic_query',
        name='generic-query'),

)
