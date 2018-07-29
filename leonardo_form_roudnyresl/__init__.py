# -*- coding: utf-8 -*-
from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _

default_app_config = 'leonardo_form_roudnyresl.Config'


class Default(object):

    optgroup = 'Roudnyresl form'

    apps = [
        'leonardo_form_roudnyresl'
    ]

    widgets = [
        'leonardo_form_roudnyresl.widget.roudnyreslform.models.RoudnyreslFormWidget'
    ]
    config = {
        'ORDER_DEFAULT_TO_EMAIL':
        ('to@email.com', u"E-mail, na který se budou odesílat objednávky."),
        'CHOICES_TYPE_PRODUCT': ('', 'JSON hodnoty'),
    }

    js_files = [
        'formset/jquery.formset.js'
    ]

    public = True


class Config(AppConfig, Default):
    name = 'leonardo_form_roudnyresl'
    verbose_name = u"Objednávky"


default = Default()
