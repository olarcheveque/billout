# -*- coding: utf-8 -*-

import datetime
from django.db import models
from django.utils.translation import ugettext as _

ENTRY_TYPES = (
    ('I', _('Income')),
    ('E', _('Expense')),
        )

class EntryCategory(models.Model):

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    name = models.CharField(max_length=255, verbose_name=_('Name'))
    type = models.CharField(max_length=3,
            verbose_name=_('Type'), choices=ENTRY_TYPES)

    def __unicode__(self):
        return u"%s (%s)" % (self.name, self.type)

    def total(self, month, year):
        date_start = datetime.date(year, month, 1)
        date_end = datetime.date(year, month+1, 1)
        entries = Entry.objects.filter(category=self, date__gte=date_start, date__lt=date_end)
        total = 0.0
        for e in entries:
            total += e.amount
        return total

    def get_total_by_month(self):
        today = datetime.date.today()
        month = today.month
        year = today.year
        date_start = datetime.date(year, 1, 1)
        date_end = datetime.date(year, month+1, 1)
        entries = Entry.objects.filter(category=self, date__gte=date_start, date__lt=date_end)
        total = {}
        for m in range(1, month+1):
            total[m] = 0.0
        for e in entries:
            total[e.date.month] += e.amount
        return total.values()

class Account(models.Model):

    class Meta:
        verbose_name = _('Account')
        verbose_name_plural = _('Accounts')

    name = models.CharField(max_length=255, verbose_name=_('Name'))

    def __unicode__(self):
        return self.name


class Entry(models.Model):

    class Meta:
        verbose_name = _('Entry')
        verbose_name_plural = _('Entries')
        ordering = ('-date', )

    date = models.DateField(verbose_name=_('Date'))
    account = models.ForeignKey('accounting.Account',
            verbose_name=_('Account'))
    category = models.ForeignKey('accounting.EntryCategory',
            verbose_name=_('Category'), related_name='entries')
    amount = models.FloatField(verbose_name=_('Amount'))
    comment = models.CharField(max_length=255, verbose_name=_('Comment'))

    def __unicode__(self):
        return u"%s %s %s %s" % (self.date, self.category, self.amount, self.comment)


class Budget(models.Model):

    class Meta:
        verbose_name = _('Budget')
        verbose_name_plural = _('Budgets')

    category = models.ForeignKey('accounting.EntryCategory',
            verbose_name=_('Category'))
    amount = models.FloatField(verbose_name=_('Amount'))

    def __unicode__(self):
        return u"%s %s" % (self.category, self.amount)

    def diff(self, month, year):
        return self.amount - self.category.total(month, year)
    
    def get_diff_by_month(self,):
        return [self.amount-m for m in self.category.get_total_by_month()]
