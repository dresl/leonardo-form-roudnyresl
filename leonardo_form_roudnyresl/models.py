# encoding: utf-8
from leonardo.module.web.models import Widget
from leonardo.module.media.fields.image import ImageField
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
import datetime
from leonardo.module.media.fields.multistorage_file import MultiStorageFileField

class RoudnyreslOrders(models.Model):

    jmeno = models.CharField(
        max_length=255, verbose_name=u"Jméno", default='')
    prijmeni = models.CharField(
        max_length=255, verbose_name=u"Příjmení", default='')
    email = models.EmailField(
        verbose_name=u"E-mail", default='')
    telefon = models.CharField(
        verbose_name=u"Telefon (ve tvaru: +420 123 456 789)", max_length=100)
    dorucovaci_adresa = models.CharField(
        verbose_name=u"Doručovací adresa", help_text="Př.: Pardubice, Benedettiho 709, 530 03", max_length=255)
    firma = models.CharField(
        max_length=255, verbose_name=u"Název firmy", default='')
    ico = models.CharField(
        verbose_name=u"IČO", max_length=255, default='')
    dic = models.CharField(
        verbose_name=u"DIČ", max_length=255, help_text="Vyplňte, jste-li plátce DPH", blank=True, null=True)
    doprava = models.CharField(
        verbose_name=u"Doprava", max_length=255)
    platba = models.CharField(
        verbose_name=u"Platba", max_length=255)
    zprava = models.TextField(
        verbose_name=u"Poznámka", default='', blank=True)
    pub_date = models.DateTimeField(u'Datum objednávky', auto_now_add=True)

    def get_full_name(self):
        return str(self.jmeno.encode("utf-8") + " " + self.prijmeni.encode("utf-8"))

    @property
    def get_absolute_url(self):
        from leonardo.module.web.widget.application.reverse import app_reverse
        return app_reverse(
            'created_order',
            'leonardo_form_roudnyresl.apps.roudnyresl',
            kwargs={
                'pk': self.id,
            })

    def __unicode__(self):
        return self.jmeno.encode("utf-8")

    class Meta:
        ordering = ['jmeno', ]
        verbose_name = u'Objednávka'
        verbose_name_plural = u'Objednávky'


class RoudnyreslProduct(models.Model):

    objednavka = models.ForeignKey(RoudnyreslOrders,
        verbose_name=u"Objednávka", related_name="orderproduct_set")
    produkt = models.CharField(
        verbose_name=u"Vyberte produkt", max_length=255)
    tloustka = models.CharField(
        verbose_name=u"Výška podstavy", max_length=255)
    vyska = models.CharField(
        verbose_name=u"Výška reliéfu", max_length=255)
    rozmer_motivu = models.CharField(
        verbose_name=u"Rozměr raženého motivu", max_length=255)
    soubor = models.FileField(
        u'Nahrání dat', upload_to='documents/%Y/%m/%d/')

    def __unicode__(self):
        return self.produkt

    class Meta:
        ordering = ['produkt', ]
        verbose_name = u'Produkt'
        verbose_name_plural = u'Produkty'
