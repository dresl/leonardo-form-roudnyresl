from django.conf.urls import patterns, url
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    url(r'^objednavka/pridat/$', views.RoudnyreslOrderCreate.as_view(), name='objedn_list'),
]
