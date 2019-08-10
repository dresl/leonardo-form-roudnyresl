# -*- coding: utf-8 -*-
from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _

try:
    from local_settings import APPS
except ImportError:
    pass

default_app_config = 'leonardo_form_roudnyresl.Config'


class Default(object):

    if 'leonardo_form_roudnyresl' in APPS:
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
            'CHOICES_TYPE_PRODUCT': ('', 'Tuple choices'),
            'CHOICES_TLOUSTKY_PODSTAVY': ('', 'Tuple choices'),
            'CHOICES_VYSKA_RELIEFU': ('', 'Tuple choices'),
            'CHOICES_DOPRAVA': ('', 'Tuple choices'),
            'CHOICES_PLATBA': ('', 'Tuple choices'),
            'INFO_PRODUCT_ORDER': ('', 'Info text'),
            'INFO_NEW_CUSTOMERS': ('', 'Info for new customers'),
        }

        @property
        def plugins(self):
            return [
                ('leonardo_form_roudnyresl.apps.roudnyresl', 'Roudnyresl form'),
        ]

        js_files = [
            'formset/jquery.formset.js',
            'js/bootstrap-select.min.js',
        ]

        css_files = [
            'css/bootstrap-select.min.css',
            'css/component.css',
        ]

        public = True


class Config(AppConfig, Default):
    name = 'leonardo_form_roudnyresl'
    verbose_name = u"Objednávky"


default = Default()
