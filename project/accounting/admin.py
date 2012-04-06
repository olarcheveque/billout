# -*- coding: utf-8 -*-

from django.contrib import admin
from models import EntryCategory, Account, Entry, Budget


class EntryCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'type',)


class AccountAdmin(admin.ModelAdmin):
    list_display = ('name',)


class EntryAdmin(admin.ModelAdmin):
    list_display = ('date', 'category', 'account', 'amount', 'comment', )


class BudgetAdmin(admin.ModelAdmin):
    list_display = ('category', 'amount',)

admin.site.register(EntryCategory, EntryCategoryAdmin)
admin.site.register(Account, AccountAdmin)
admin.site.register(Entry, EntryAdmin)
admin.site.register(Budget, BudgetAdmin)
