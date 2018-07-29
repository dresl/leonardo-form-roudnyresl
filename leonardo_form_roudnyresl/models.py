# encoding: utf-8
from leonardo.module.web.models import Widget
from leonardo.module.media.fields.image import ImageField
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
import datetime
from leonardo.module.media.fields.multistorage_file import MultiStorageFileField

try:
    import simplejson as json
except ImportError:
    import json

# data = json.load(settings.CHOICES_TYPE_PRODUCT)
# print(tuple(data.items()))

class RoudnyreslOrders(models.Model):

    jmeno = models.CharField(
        max_length=255, verbose_name=u"Jméno", default='')
    prijmeni = models.CharField(
        max_length=255, verbose_name=u"Příjmení", default='')
    telefon = models.CharField(
        verbose_name=u"Telefon (ve tvaru: +420 123 456 789)", max_length=100)
    email = models.EmailField(
        verbose_name=u"E-mail", default='')
    dorucovaci_adresa = models.CharField(
        verbose_name=u"Doručovací adresa", help_text="Př.: Pardubice, Benedettiho 709, 530 03", max_length=255)
    ico = models.CharField(
        verbose_name=u"IČO", max_length=255)
    dic = models.CharField(
        verbose_name=u"DIČ", max_length=255, blank=True, null=True)
    zprava = models.TextField(
        verbose_name=u"Poznámka", default='', blank=True)
    pub_date = models.DateTimeField(u'Datum objednávky', auto_now_add=True)

    def __unicode__(self):
        return self.jmeno

    class Meta:
        ordering = ['jmeno', ]
        verbose_name = u'Objednávka'
        verbose_name_plural = u'Objednávky'


class RoudnyreslProduct(models.Model):

    objednavka = models.ForeignKey(RoudnyreslOrders,
        verbose_name=u"Objednávka", related_name="orderproduct_set")
    produkt = models.PositiveIntegerField(
        verbose_name=u"Vyberte produkt", default=1)
    tloustka = models.CharField(
        verbose_name=u"Tloušťka podstavy", choices=CHOICES_TYPE_MATERIALY, max_length=255)
    vyska = models.CharField(
        verbose_name=u"Šířka podstavy", choices=CHOICES_TYPE_LAMINACE, max_length=255)
    rozmer_motivu = models.CharField(
        verbose_name=u"Rozměr raženého motivu", choices=CHOICES_TYPE_LAMINACE, max_length=255)
    soubor = models.FileField(
        u'Soubor', upload_to='documents/%Y/%m/%d/')

    def __unicode__(self):
        return self.produkt

    class Meta:
        ordering = ['produkt', ]
        verbose_name = u'Produkt'
        verbose_name_plural = u'Produkty'
