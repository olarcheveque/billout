# -*- encoding: utf-8 -*-

from django.core.urlresolvers import reverse
from django.db.models import Q
from django.contrib.auth.models import User as Customer
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.template import Context, RequestContext
from django.utils.translation import ugettext as _
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.conf import settings
from models import Bill, BILL_PUBLISHED

@login_required
def bills(request, username=None):
    balance = 0

    if request.user.is_superuser and username is not None:
        customer = Customer.objects.get(username=username)
        customers = Customer.objects.all()
        q = Q(state=BILL_PUBLISHED) & Q(customer=customer)

    if request.user.is_superuser and username is None:
        customer = None
        customers = Customer.objects.all()
        q = Q(state=BILL_PUBLISHED)

    if request.user.is_superuser is None:
        customer = request.user
        customers = Customer.objects.none()
        q = Q(state=BILL_PUBLISHED) & Q(customer=customer)

    bills = Bill.objects.filter(q)
    for bill in Bill.objects.filter(q & Q(payed=False)):
        balance += bill.total_with_taxes()
        
    c = {
        'customers' : customers,
        'customer' : customer,
        'balance' : balance,
        'bills' : bills.order_by('-date', '-id'), 
    }
    return render_to_response("billout/bills.html", \
                               Context(c), \
                               context_instance = RequestContext(request))

@login_required
def bill(request, id):
    bill = get_object_or_404(Bill, id=id)
    if request.user != bill.customer and not request.user.is_superuser:
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
