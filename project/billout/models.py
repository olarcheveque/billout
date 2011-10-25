# -*- encoding: utf-8 -*-

from django.core.mail import send_mail
from django.utils.translation import ugettext as _
from django.template.loader import render_to_string
from django.conf import settings
from django.db import models

CANADA_CODE = 'CA'
QUEBEC_CODE = 'QC'

class Project(models.Model):
    customer = models.ForeignKey('auth.User', verbose_name=_('Customer'))
    name = models.CharField(max_length=255, verbose_name=_('Name'))

    class Meta:
        verbose_name = _('Project')
        verbose_name_plural = _('Projects')

    def __unicode__(self):
        return u"[%s] %s" % (self.customer, self.name)

class ActivityManager(models.Manager):
    def get_query_set(self):
        activities_linked_to_item = [i.activity.id for i in Item.objects.all()]
        return super(ActivityManager, self).get_query_set().exclude(id__in=activities_linked_to_item)

class Activity(models.Model):
    objects = ActivityManager()
    customer = models.ForeignKey('auth.User', verbose_name=_('Customer'))
    date = models.DateField(verbose_name=_('Date'))
    project = models.ForeignKey('Project', verbose_name=_('Project'), blank=True, null=True)
    hours = models.FloatField(verbose_name=_('Hours'))
    comment = models.CharField(max_length=255, verbose_name=_('Comment'))

    class Meta:
        verbose_name = _('Activity')
        verbose_name_plural = _('Activities')

    def __unicode__(self):
        if self.project is not None:
            project = self.project.name
        else:
            project = u"-"
        return u"[%s %s] %s %sH" % (self.customer, project, self.comment, self.hours)


class Rate(models.Model):
    name = models.CharField(max_length=255, verbose_name=_('Name'))
    hour_price = models.FloatField(verbose_name=_('Hour price')) 

    class Meta:
        verbose_name = _('Rate')
        verbose_name_plural = _('Rates')

    def __unicode__(self):
        return u"%s %s" % (self.name, self.hour_price)

# syncdb
try:
    RATE_CHOICES = [(r.hour_price, r.__unicode__()) for r in Rate.objects.all()]
except:
    RATE_CHOICES = ()

class Item(models.Model):
    bill = models.ForeignKey('Bill', verbose_name=_('Bill'))
    activity = models.ForeignKey('Activity', verbose_name=_('Activity'), null=True)
    rate = models.FloatField(verbose_name=_('Rate'), choices=RATE_CHOICES)
    tps = models.BooleanField(verbose_name=_('TPS'), default=True)
    tvq = models.BooleanField(verbose_name=_('TVQ'), default=True)

    class Meta:
        verbose_name = _('Item')
        verbose_name_plural = _('Items')

    def __unicode__(self):
        return self.activity.__unicode__()


class Bill(models.Model):
    date = models.DateField(auto_now_add=True, verbose_name=_('Date'))
    customer = models.ForeignKey('auth.User', verbose_name=_('Customer'))
    payed = models.BooleanField(verbose_name=_('Payed'), default=False)

    class Meta:
        verbose_name = _('Bill')
        verbose_name_plural = _('Bills')

    def __unicode__(self):
        return "#%s %s (%s)" % (self.id, self.customer, self.date)

    def total_without_taxes(self):
        total = 0
        items = Item.objects.filter(bill=self)
        for i in items:
            total += i.activity.hours * i.rate
        return round(total, 2)

    def total_tps(self):
        total = 0
        items = [i for i in Item.objects.filter(bill=self) if i.tps]
        for i in items:
            total += i.activity.hours * i.rate * settings.TPS_RATE
        return round(total, 2)

    def total_tvq(self):
        total = 0
        items = [i for i in Item.objects.filter(bill=self) if i.tps]
        for i in items:
            base = i.activity.hours * i.rate
            total +=  (base + base * settings.TPS_RATE) * settings.TVQ_RATE
        return round(total, 2)

    def total_with_taxes(self):
        return self.total_without_taxes() + self.total_tps() + self.total_tvq()

    def mail(self):
        company = getattr(settings, 'BILLOUT_COMPANY_NAME', 'BILLOUT')
        subject = u"%s : Facture / Bill #%s" % (company, self.id, )
        sender = getattr(settings, 'BILLOUT_SENDER_EMAIL', 'noreply@billout')
        message = render_to_string('billout/mail.html', { 'bill' : self })
        email = self.customer.email
        if email in (None, ''):
            raise Exception(_("No email set for customer"))
        copies =  getattr(settings, 'BILLOUT_EMAIL_COPIES', [])
        to = [email,] + copies
        send_mail(subject, message, sender, to, fail_silently=False)
