# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib.auth import logout as auth_logout
from django.contrib.sites.models import Site
from django.shortcuts import redirect
from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.utils.decorators import method_decorator
from django.shortcuts import render
from leonardo.decorators import require_auth
from django.db import transaction
from leonardo import forms, messages
from django.forms import widgets
from django.core.urlresolvers import reverse_lazy
from django.forms import inlineformset_factory
from .models import RoudnyreslOrders, RoudnyreslProduct
from .forms import RoudnyreslOrderFormSet
from django.views.generic import CreateView, DetailView, ListView
from leonardo.utils.emails import send_templated_email as send_mail
from .form_choices import *


class RoudnyreslOrderCreate(CreateView):
    model = RoudnyreslOrders
    fields = ['jmeno', 'prijmeni', 'email',
            'telefon', 'dorucovaci_adresa', 'firma',
            'ico', 'dic', 'doprava', 'platba', 'zprava']

    def get_form(self, form_class):
        form = super(RoudnyreslOrderCreate, self).get_form(form_class)
        for field in form.fields:
            if field == "doprava":
                form.fields[field].widget = widgets.Select(choices=CHOICES_DOPRAVA)
            elif field == "platba":
                form.fields[field].widget = widgets.Select(choices=CHOICES_PLATBA)
            elif field == "zprava":
                form.fields[field].widget = widgets.Textarea(attrs={'rows':5})
            elif field != "dic":
                form.fields[field].widget = widgets.TextInput(attrs={"required": "true"})
        return form

    def get_context_data(self, **kwargs):
        data = super(RoudnyreslOrderCreate, self).get_context_data(**kwargs)
        if self.request.POST:
            data['orderproducts'] = RoudnyreslOrderFormSet(self.request.POST, self.request.FILES)
        else:
            data['orderproducts'] = RoudnyreslOrderFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        orderproducts = context['orderproducts']
        with transaction.atomic():
            self.object = form.save()
            if orderproducts.is_valid():
                orderproducts.instance = self.object
                orderproducts.save()
                current_order = RoudnyreslOrders.objects.get(id=orderproducts.instance.id,)
                subject_order = "Objednávka - " + current_order.get_full_name()
                send_mail(
                    subject_order,
                    'leonardo_form_roudnyresl/roudnyresl_email.html', {
                        'order_title': "Objednávka",
                        'order': current_order,
                        'site': self.request.site,
                    },
                    [email.strip() for email in settings.ORDER_DEFAULT_TO_EMAIL.split(',')],
                    settings.DEFAULT_FROM_EMAIL,
                    fail_silently=False,
                )
                # send confirmation
                send_mail(
                    'Potvrzení o objednávce štočků',
                    'leonardo_form_roudnyresl/roudnyresl_email.html', {
                        'order_title': "Potvrzení o objednávce",
                        'order': current_order,
                        'site': self.request.site,
                    },
                    current_order.email,
                    fail_silently=False,
                )
                return HttpResponseRedirect("objednavka/%s" % self.object.id)
        return super(RoudnyreslOrderCreate, self).form_valid(form)


class CreatedOrderInfo(DetailView):
    model = RoudnyreslOrders
    template_name = "leonardo_form_roudnyresl/created_order_info.html"

    def get_context_data(self, **kwargs):
        data = super(CreatedOrderInfo, self).get_context_data(**kwargs)
        data["order_title"] = "Shrnutí objednávky"
        return data
