from django.conf.urls import url
from leonardo_form_roudnyresl.views import RoudnyreslOrderCreate, CreatedOrderInfo


def roudnyresl_patterns(list_kwargs={}, detail_kwargs={}):
    return [
        url(r'^$',
            RoudnyreslOrderCreate.as_view(**list_kwargs), name='objedn_list'),
        url(r'^objednavka/(?P<pk>\d+)/$',
            CreatedOrderInfo.as_view(), name='created_order'),
    ]

urlpatterns = roudnyresl_patterns()
