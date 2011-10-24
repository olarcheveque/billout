# -*- encoding: utf-8 -*-

from django.utils.translation import ugettext as _
from django.contrib import admin
from models import *

class ItemInline(admin.TabularInline):
    model = Item

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'customer',  )

class ActivityAdmin(admin.ModelAdmin):
    list_display = ('date', 'customer', 'project', 'hours', 'comment',  )
    list_filter = ('customer', 'project', )

class RateAdmin(admin.ModelAdmin):
    pass

class BillAdmin(admin.ModelAdmin):
    list_editable = ('payed', )
    list_display = ('id', 'date', 'customer', '_total_without_taxes', '_total_tps', '_total_tvq', '_total_with_taxes', 'payed', )
    list_filter = ('customer', )
    inlines = (ItemInline, )

    def _total_without_taxes(self, obj):
        return obj.total_without_taxes()
    _total_without_taxes.short_description = _('Total without taxes')

    def _total_tps(self, obj):
        return obj.total_tps()
    _total_tps.short_description = _('TPS')

    def _total_tvq(self, obj):
        return obj.total_tvq()
    _total_tvq.short_description = _('TVQ')

    def _total_with_taxes(self, obj):
        return obj.total_with_taxes()
    _total_with_taxes.short_description = _('Total with taxes')

admin.site.register(Project, ProjectAdmin)
admin.site.register(Activity, ActivityAdmin)
admin.site.register(Bill, BillAdmin)
admin.site.register(Rate, RateAdmin)
