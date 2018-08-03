# encoding: utf-8
from django.contrib import admin
from django.conf import settings
from leonardo_form_roudnyresl.models import RoudnyreslOrders, RoudnyreslProduct


class RoudnyreslProductsInline(admin.TabularInline):
    model = RoudnyreslProduct
    extra = 1


class RoudnyreslOrdersAdmin(admin.ModelAdmin):
    model = RoudnyreslOrders
    inlines = [RoudnyreslProductsInline]
    list_display = ('prijmeni', 'pub_date')
    list_filter = ['pub_date','prijmeni']
    search_fields = ['prijmeni']
    readonly_fields = ['pub_date']


admin.site.register(RoudnyreslOrders, RoudnyreslOrdersAdmin)
