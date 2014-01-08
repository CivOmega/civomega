from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

urlpatterns = patterns('',
    url(r'^$', TemplateView.as_view(template_name="index.html"), name='homepage'),
    url(r'^ask$', 'civomega.codata.views.ask', name='ask'),

)
