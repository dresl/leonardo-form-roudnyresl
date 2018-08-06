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
from django.forms import widgets
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from horizon.utils import validators
from horizon_contrib.forms import SelfHandlingModelForm
from django.forms import inlineformset_factory
from django.db import models
from django.forms import Field as DjangoField
from .models import RoudnyreslOrders, RoudnyreslProduct
from django.conf import settings
from horizon import forms, messages
from .form_choices import *


class BaseInlineRoudnyreslFormSet(django_forms.BaseInlineFormSet):
    def clean(self):
     """Checks that no two articles have the same title."""
     if any(self.errors):
         # Don't bother validating the formset unless each form is valid on its own
         return
     titles = []
     for form in self.forms:
         title = form.cleaned_data['produkt']
         if title in titles:
             raise forms.ValidationError("Articles in a set must have distinct titles.")
         titles.append(title)

DjangoField.default_error_messages = {
    'required': "Toto pole je povinné.",
    'invalid': "Zadejte správný formát e-mailu."
}

class RoudnyreslOrderForm(django_forms.ModelForm):
    class Meta:
        model = RoudnyreslProduct
        exclude = ()

RoudnyreslOrderFormSet = inlineformset_factory(RoudnyreslOrders, RoudnyreslProduct,
                                            widgets={
                                                'produkt': widgets.Select(choices=CHOICES_TYPE_PRODUCT),
                                                'tloustka': widgets.Select(choices=CHOICES_TLOUSTKY_PODSTAVY),
                                                'vyska': widgets.Select(choices=CHOICES_VYSKA_RELIEFU),
                                                'rozmer_motivu': widgets.TextInput(attrs={
                                                    "class": "form-control",
                                                    "required": "true",
                                                    }),
                                                'soubor': widgets.FileInput(attrs={
                                                    "required": "true",
                                                    }),
                                            },
                                            form=RoudnyreslOrderForm, extra=1,
                                            formset=BaseInlineRoudnyreslFormSet)
