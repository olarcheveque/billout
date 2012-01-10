# -*- encoding: utf-8 -*-

from django.core.urlresolvers import reverse
from django.db.models import Q
from django.contrib.auth.models import User as Customer
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.template import Context, RequestContext
from django.utils.translation import ugettext as _
from django.shortcuts import render_to_response, redirect, get_object_or_404
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
    bills = Bill.objects.filter(q).order_by('-date')

    annual_reports = {}

    for bill in bills:
        if not annual_reports.has_key(bill.date.year):
            annual_reports[bill.date.year] = {
                'hours' : 0.0,
                'tps' : 0.0,
                'tvq' : 0.0,
                'total_without_taxes' :  0.0,
                'total_with_taxes' :  0.0,
            }
        annual_reports[bill.date.year]['hours'] += bill.total_worked_hours()
        annual_reports[bill.date.year]['tps'] += bill.total_tps()
        annual_reports[bill.date.year]['tvq'] += bill.total_tvq()
        annual_reports[bill.date.year]['total_without_taxes'] += bill.total_without_taxes()
        annual_reports[bill.date.year]['total_with_taxes'] += bill.total_with_taxes()

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
    
    c = {
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
