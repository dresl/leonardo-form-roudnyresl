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
from django.core.urlresolvers import reverse_lazy
from django.forms import inlineformset_factory
from .models import RoudnyreslOrders, RoudnyreslProducts
from .forms import RoudnyreslOrderFormSet
from django.views.generic import CreateView
from leonardo.utils.emails import send_templated_email as send_mail


class RoudnyreslOrderCreate(forms.ModalFormView, forms.views.CreateView):
    model = RoudnyreslOrders
    template_name = "leonardo_form_roudnyresl/roudnyreslorders_form.html"
    submit_label = "Objednat"

    def get_context_data(self, **kwargs):
        ret = super(RoudnyreslOrderCreate, self).get_context_data(**kwargs)
        if self.request.method == 'POST':
            ret['orderproducts'] = RoudnyreslOrderFormSet(self.request.POST,self.request.FILES)
        else:
            ret['orderproducts'] = RoudnyreslOrderFormSet()

        ret.update({
            "view_name": "Objednávací formulář",
            "modal_size": 'lg fullscreen',
            "modal_header": 'Objednávací formulář',
            })
        return ret


    def form_valid(self, form):
        context = self.get_context_data()
        orderproducts = context['orderproducts']
        with transaction.atomic():
            self.object = form.save()
            if orderproducts.is_valid():
                orderproducts.instance = self.object
                orderproducts.save()
                prijmeni_text = orderproducts.data['prijmeni']
                current_order = RoudnyreslOrders.objects.get(id=orderproducts.instance.id,)
                subject_order = u"Objednávka - " + prijmeni_text
                send_mail(
                    subject_order,
                    'leonardo_form_roudnyresl/roudnyresl_email.html', {
                        'order_title': u"Objednávka",
                        'order': current_order,
                        'domain': Site.objects.get(request.site.name)
                    },
                    [email.strip() for email in settings.ORDER_DEFAULT_TO_EMAIL.split(',')],
                    fail_silently=False,
                )
                subject_confirmation = u"Potvrzení o objednávce - " + request.site.name
                send_mail(
                    subject_confirmation,
                    'leonardo_form_roudnyresl/roudnyresl_email.html', {
                        'order_title': u"Potvrzení o objednávce",
                        'order': current_order,
                        'domain': Site.objects.get(name=request.site.name)
                    },
                    current_order.email,
                    fail_silently=False,
                )

        return super(RoudnyreslOrderCreate, self).form_valid(form)

