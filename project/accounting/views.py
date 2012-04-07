# -*- coding: utf-8 -*-

import datetime
from django.views.generic import ListView
from models import Budget

class BudgetView(ListView):

    context_object_name = "publisher"
    model = Budget

    def get_context_data(self, **kwargs):
        context = super(BudgetView, self).get_context_data(**kwargs)

        headers = []
        today = datetime.date.today()
        year = today.year

        for month in range(1, today.month+1):
            label = u"%s-%s" % (month, year)
            headers.append(label)
        
        context['headers'] = headers
        return context

