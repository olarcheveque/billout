# -*- encoding: utf-8 -*-

from django.utils.translation import ugettext as _
from django.forms.models import BaseInlineFormSet
from django.contrib import admin, messages
from models import *

class ItemInlineFormset(BaseInlineFormSet):
    def add_fields(self, form, index):
        super(ItemInlineFormset, self).add_fields(form, index)
        activities_linked_to_item = [i.activity.id for i in Item.objects.all()]
        selected = form.initial.get('activity')
        if selected is not None:
            activities_linked_to_item.remove(selected)
        qs = Activity.objects.exclude(id__in=activities_linked_to_item)
        form.fields['activity'].queryset = qs
        print selected

class ItemInline(admin.TabularInline):
    model = Item
    formset = ItemInlineFormset

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'customer',  )

class ActivityAdmin(admin.ModelAdmin):
    search_fields = ('date', 'comment', )
    list_display = ('date', 'customer', 'project', 'hours', 'comment',  '_charged')
    list_filter = ('customer', 'project', )

    def _charged(self, obj):
        if obj.item_set is not None:
            return ", ".join([i.bill.__unicode__() for i in obj.item_set.all()])
    _charged.short_description = _("Charged")

class RateAdmin(admin.ModelAdmin):
    pass

def mail_bill(modeladmin, request, queryset):
    selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
    for bill in Bill.objects.filter(id__in=selected):
        try:
            bill.mail()
            messages.add_message(request, messages.SUCCESS, _("Bill sent"))
        except Exception, e:
            messages.add_message(request, messages.ERROR, e)


class BillAdmin(admin.ModelAdmin):
    list_editable = ('payed', )
    list_display = ('id', 'date', 'customer', '_total_without_taxes', '_total_tps', '_total_tvq', '_total_with_taxes', 'payed', )
    list_filter = ('customer', )
    actions = [mail_bill, ]
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
