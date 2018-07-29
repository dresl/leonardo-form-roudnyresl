# encoding: utf-8
from django.contrib import admin
from django.conf import settings
from leonardo_form_roudnyresl.models import RoudnyreslOrders, PegastudioProducts


class PegastudioProductsInline(admin.TabularInline):
    model = RoudnyreslOrders
    extra = 1


class RoudnyreslOrdersAdmin(admin.ModelAdmin):
    model = RoudnyreslOrders
    def get_readonly_fields(self, request, obj=None):
        if obj is None:
            return ['pub_date']
        else:
            return ['pub_date']
        return []
    inlines = [PegastudioProductsInline]
    list_display = ('prijmeni', 'pub_date')
    list_filter = ['pub_date','prijmeni']
    search_fields = ['prijmeni']


admin.site.register(RoudnyreslOrders, RoudnyreslOrdersAdmin)