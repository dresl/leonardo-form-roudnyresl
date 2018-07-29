# -*- coding: utf-8 -*-
from __future__ import absolute_import

from django.utils import timezone

from crispy_forms.layout import \
    HTML, Field, Layout, Fieldset, MultiField, Div, Submit, ButtonHolder
from crispy_forms.bootstrap import PrependedText
from django.contrib.auth import authenticate, get_user_model, login
from django.contrib.auth.models import User
from django.contrib.auth.tokens import \
    default_token_generator as token_generator
from django import forms as django_forms
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from horizon.utils import validators
from horizon_contrib.forms import SelfHandlingModelForm
from django.forms import inlineformset_factory
from django.db import models
from django.forms import Field as DjangoField
from .models import RoudnyreslOrders, RoudnyreslProducts
from django.conf import settings
from horizon import forms, messages


DjangoField.default_error_messages = {
    'required': "Toto pole je povinné.",
    'invalid': "Zadejte správný formát e-mailu."
}

def my_handle(self, request, data):

    instance = self.save()

    messages.success(request, u"Objednávka úspěšně dokončena.")
    if hasattr(self, 'handle_related_models'):
        # handle related models
        self.handle_related_models(self.request, instance)

    return instance

SelfHandlingModelForm.handle = my_handle


class RoudnyreslOrderForm(SelfHandlingModelForm):

    class Meta:
        model = RoudnyreslOrders
        exclude = ()


RoudnyreslOrderFormSet = inlineformset_factory(RoudnyreslOrders, RoudnyreslProducts, extra=1, fields=['pocet_kusu','laminace','material','file'])
