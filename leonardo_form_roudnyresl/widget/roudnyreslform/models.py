# -#- coding: utf-8 -#-

from django.db import models
from django.utils.translation import ugettext_lazy as _
from leonardo.module.web.models import Widget
from leonardo_form_roudnyresl.models import RoudnyreslOrders


class RoudnyreslFormWidget(Widget):

    def get_items(self):
        return RoudnyreslOrders.objects.all().order_by("-pub_date")

    class Meta:
        abstract = True
        verbose_name = _('Roudnyresl module')
        verbose_name_plural = _('Roudnyresl modules')
