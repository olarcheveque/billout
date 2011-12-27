# -*- encoding: utf-8 -*-

from django.core.mail import send_mail
from django.utils.translation import ugettext as _
from django.template import Context, Template
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


class Activity(models.Model):
    customer = models.ForeignKey('auth.User', verbose_name=_('Customer'))
    date = models.DateField(verbose_name=_('Date'))
    project = models.ForeignKey('Project', verbose_name=_('Project'), blank=True, null=True)
    hours = models.FloatField(verbose_name=_('Hours'))
    comment = models.CharField(max_length=255, verbose_name=_('Comment'))

    class Meta:
        ordering = ['-date', ]
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

BILL_DRAFT = 'draft'
BILL_PUBLISHED = 'published'
BILL_STATE_CHOICES = (
    (BILL_DRAFT, _("Draft")),
    (BILL_PUBLISHED, _("Published")),
)
class Bill(models.Model):
    date = models.DateField(verbose_name=_('Date'))
    customer = models.ForeignKey('auth.User', verbose_name=_('Customer'))
    payed = models.BooleanField(verbose_name=_('Payed'), default=False)
    state = models.CharField(max_length=10, verbose_name=_('State'), choices=BILL_STATE_CHOICES)

    class Meta:
        verbose_name = _('Bill')
        verbose_name_plural = _('Bills')

    def __unicode__(self):
        return "#%s %s (%s)" % (self.id, self.customer, self.date)

    def total_worked_hours(self):
        total = 0
        items = Item.objects.filter(bill=self)
        for i in items:
            total += i.activity.hours
        return round(total, 2)

    def total_without_taxes(self):
        total = 0
        items = Item.objects.filter(bill=self)
        for i in items:
            total += i.activity.hours * i.rate
        return round(total, 2)

    def get_tps_rate(self):
        try:
            return Tax.objects.get(name='TPS', year=self.date.year).value
        except Tax.DoesNotExist:
            raise Exception("%s : %s" % (_('There is no TPS rate for year '),  self.date.year))

    def get_tvq_rate(self):
        try:
            return Tax.objects.get(name='TVQ', year=self.date.year).value
        except Tax.DoesNotExist:
            raise Exception("%s : %s" % (_('There is no TVQ rate for year '),  self.date.year))

    def total_tps(self):
        tps_rate = self.get_tps_rate()
        total = 0
        items = [i for i in Item.objects.filter(bill=self) if i.tps]
        for i in items:
            total += i.activity.hours * i.rate * tps_rate
        return round(total, 2)

    def total_tvq(self):
        tps_rate = self.get_tps_rate()
        tvq_rate = self.get_tvq_rate()
        total = 0
        items = [i for i in Item.objects.filter(bill=self) if i.tps]
        for i in items:
            base = i.activity.hours * i.rate
            total +=  (base + base * tps_rate) * tvq_rate
        return round(total, 2)

    def total_with_taxes(self):
        return self.total_without_taxes() + self.total_tps() + self.total_tvq()

    def mail(self):
        company = Setting.objects.val("COMPANY_NAME")
        subject = Setting.objects.val("BILL_SUBJECT") % (company, self.id)
        sender = Setting.objects.val("BILL_SENDER")
        mail_content = Setting.objects.val("BILL_MAIL_CONTENT")
        t = Template(mail_content)
        c = Context({
            "bill": self,
        })
        message = t.render(c)
        email = self.customer.email
        if email in (None, ''):
            raise Exception(_("No email set for customer"))
        copies = [c.strip() for c in Setting.objects.val("BILL_MAIL_COPIES").split(',')]
        to = [email,] + copies
        send_mail(subject, message, sender, to, fail_silently=False)


class SettingManager(models.Manager):
    def val(self, key):
        try:
            return self.get(key=key).value
        except:
            raise Exception("%s : %s" % (_("Setting key is not defined"), key))


class Setting(models.Model):
    objects = SettingManager()
    key = models.CharField(max_length=255, verbose_name=_('Key'))
    name = models.CharField(max_length=255, verbose_name=_('Name'))
    value = models.TextField(verbose_name=_('Value'), null=True )

    class Meta:
        verbose_name = _('Setting')
        verbose_name_plural = _('Settings')


class Tax(models.Model):
    name = models.CharField(max_length=255, verbose_name=_('Name'))
    value = models.FloatField(verbose_name=_('Value'),)
    year = models.IntegerField(verbose_name=_('Year'),)

    class Meta:
        verbose_name = _('Tax')
        verbose_name_plural = _('Taxes')
