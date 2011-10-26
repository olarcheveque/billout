# -*- encoding: utf-8 -*-

from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('billout.views',
    url(r'^bills/(?P<username>\w+)/$', 'bills', name='bills'),
    url(r'^bills/$', 'bills', name='bills'),
    url(r'^bill/(?P<id>\d+)$', 'bill', name='bill'),
)
