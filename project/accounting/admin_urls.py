# -*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns, url
from django.views.generic.simple import direct_to_template
from views import BudgetView

urlpatterns = patterns('views',
    url(r'^accounting/overview/$', BudgetView.as_view(),
        name="budget",
    ),
    )
