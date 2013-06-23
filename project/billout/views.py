# -*- encoding: utf-8 -*-

from datetime import datetime

from django.core.urlresolvers import reverse
from django.db.models import Q
from django.template import Context, RequestContext
from django.utils.translation import ugettext as _
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.conf import settings

from django.contrib.auth.models import User as Customer
from django.contrib.auth.decorators import login_required
from django.contrib import messages

import stripe

from models import Bill, BILL_PUBLISHED, Setting


def _get_context_qs_vars(request, username=None):
    """
    Load bills for admin or customer
    """
    if request.user.is_superuser and username is not None:
        customer = Customer.objects.get(username=username)
        customers = Customer.objects.all()
        q = Q(state=BILL_PUBLISHED) & Q(customer=customer)

    if request.user.is_superuser and username is None:
        customer = None
        customers = Customer.objects.all()
        q = Q(state=BILL_PUBLISHED)

    if request.user.is_superuser is False:
        customer = request.user
        customers = Customer.objects.none()
        q = Q(state=BILL_PUBLISHED) & Q(customer=customer)
    return customers, customer, q


@login_required
def reports(request, username=None):
    customers, customer, q = _get_context_qs_vars(request, username)
    bills = Bill.objects.filter(q)

    annual_reports = {}

    for bill in bills:
        year = int(bill.date.year)
        if not annual_reports.has_key(year):
            annual_reports[year] = {
                'hours' : 0.0,
                'tps' : 0.0,
                'tvq' : 0.0,
                'total_without_taxes' :  0.0,
                'total_with_taxes' :  0.0,
            }
        annual_reports[year]['hours'] += bill.total_worked_hours()
        annual_reports[year]['tps'] += bill.total_tps()
        annual_reports[year]['tvq'] += bill.total_tvq()
        annual_reports[year]['total_without_taxes'] += bill.total_without_taxes()
        annual_reports[year]['total_with_taxes'] += bill.total_with_taxes()
    
    annual_reports = sorted(annual_reports.iteritems(), reverse=True)

    c = {
        'annual_reports' : annual_reports,
        'customers' : customers,
        'customer' : customer,
    }
    return render_to_response("billout/reports.html", \
                               Context(c), \
                               context_instance = RequestContext(request))

@login_required
def bills(request, username=None):
    customers, customer, q = _get_context_qs_vars(request, username)
    bills = Bill.objects.filter(q)

    balance = 0
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
    
    stripe_amount = int(bill.total_with_taxes() * 100)

    if request.method == 'POST':
        stripe.api_key = settings.STRIPE_SECRET
        token = request.POST['stripeToken']
        try:
            charge = stripe.Charge.create(
                        amount=stripe_amount,
                        currency="cad",
                        card=token,
                        description=u"%s%s" % (settings.STRIPE_PREFIX, bill.id),
                        )
            bill.payed = True
            bill.date_payed = datetime.now()
            bill.save()
        except stripe.CardError, e: # The card has been declined
            pass
        

    c = {
        'STRIPE_KEY' : settings.STRIPE_KEY,
        'STRIPE_AMOUNT' : stripe_amount,
        'STRIPE_DESC' : u"%s #%s" % (_("Bill"), bill.id ),
        'TPS_NUM' : Setting.objects.val("TPS_NUM"),
        'TVQ_NUM' : Setting.objects.val("TVQ_NUM"),
        'PAY_INFO' : Setting.objects.val("PAY_INFO"),
        'ADDRESS' : Setting.objects.val("ADDRESS"),
        'tps_rate' : bill.get_tps_rate() * 100,
        'tvq_rate' : bill.get_tvq_rate() * 100,
        'bill' : bill,
        'items' : bill.items.all().order_by('activity__date'),
    }
    return render_to_response("billout/bill.html", \
                               Context(c), \
                               context_instance = RequestContext(request))
