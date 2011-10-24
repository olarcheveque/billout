# -*- encoding: utf-8 -*-

from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.template import Context, RequestContext
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.conf import settings
from models import Bill

@login_required
def bills(request, ):
    if request.user.is_superuser:
        bills = Bill.objects.all()
    else:
        bills = Bill.objects.filter(customer=request.user)

    c = {
        'bills' : bills.order_by('date'), 
    }
    return render_to_response("billout/bills.html", \
                               Context(c), \
                               context_instance = RequestContext(request))

@login_required
def bill(request, id):
    bill = get_object_or_404(Bill, id=id)
    if request.user != bill.customer:
        messages.add_message(request, messages.ERROR, _("Don't try to spy please."))
        return redirect(reverse('bills'))
    
    c = {
        'TPS_NUM' : settings.TPS_NUM,
        'TVQ_NUM' : settings.TVQ_NUM,
        'PAY_TO' : settings.PAY_TO,
        'ADDRESS' : settings.ADDRESS,
        'bill' : bill,
    }
    return render_to_response("billout/bill.html", \
                               Context(c), \
                               context_instance = RequestContext(request))