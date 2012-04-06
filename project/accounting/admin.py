# -*- coding: utf-8 -*-

from django.contrib import admin
from models import EntryCategory, Account, Entry


class EntryCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'type',)


class AccountAdmin(admin.ModelAdmin):
    list_display = ('name',)


class EntryAdmin(admin.ModelAdmin):
    list_display = ('date', 'category', 'account', 'comment', )

admin.site.register(EntryCategory, EntryCategoryAdmin)
admin.site.register(Account, AccountAdmin)
admin.site.register(Entry, EntryAdmin)
