from django.conf.urls import url
from leonardo_form_roudnyresl.views import RoudnyreslOrderCreate


def roudnyresl_patterns(list_kwargs={}, detail_kwargs={}):
    return [
        url(r'^$',
            RoudnyreslOrderCreate.as_view(**list_kwargs), name='objedn_list'),
    ]

urlpatterns = roudnyresl_patterns()
