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
from django.views.generic import CreateView, ListView
from leonardo.utils.emails import send_templated_email as send_mail
from .form_choices import *


class RoudnyreslOrderCreate(CreateView):
    model = RoudnyreslOrders
    fields = ['jmeno', 'prijmeni', 'email',
            'telefon', 'dorucovaci_adresa', 'firma',
            'ico', 'dic', 'doprava', 'platba', 'zprava']

    success_url = "/"

    def get_form(self, form_class):
        form = super(RoudnyreslOrderCreate, self).get_form(form_class)
        form.fields['doprava'].widget = widgets.Select(choices=CHOICES_DOPRAVA)
        form.fields['platba'].widget = widgets.Select(choices=CHOICES_PLATBA)
        form.fields['zprava'].widget = widgets.Textarea(attrs={'rows':5})
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
        return super(RoudnyreslOrderCreate, self).form_valid(form)

