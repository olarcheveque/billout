# -*- coding: utf-8 -*-

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


class Account(models.Model):

    class Meta:
        verbose_name = _('Account')
        verbose_name_plural = _('Accounts')

    name = models.CharField(max_length=255, verbose_name=_('Name'))


class Entry(models.Model):

    class Meta:
        verbose_name = _('Entry')
        verbose_name_plural = _('Entries')

    date = models.DateField(verbose_name=_('Date'))
    account = models.ForeignKey('accounting.Account',
            verbose_name=_('Account'))
    category = models.ForeignKey('accounting.EntryCategory',
            verbose_name=_('Category'))
    amount = models.FloatField(verbose_name=_('Amount'))
    comment = models.CharField(max_length=255, verbose_name=_('Comment'))

class Budget(models.Model):

    class Meta:
        verbose_name = _('Budget')
        verbose_name_plural = _('Budgets')

    category = models.ForeignKey('accounting.EntryCategory',
            verbose_name=_('Category'))
    amount = models.FloatField(verbose_name=_('Amount'))
