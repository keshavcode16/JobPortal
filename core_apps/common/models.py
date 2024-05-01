from datetime import datetime
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.conf import settings
from django.utils.text import slugify
from mptt.models import MPTTModel, TreeForeignKey
from core_apps.authentication.models import User
from django_extensions.db.fields import json
from django_countries.fields import CountryField
from django.utils.translation import gettext_lazy as _
import shortuuid
import uuid




def mobile_icon_directory_path(instance, filename):
    s = shortuuid.ShortUUID(alphabet="0123456789")
    rnd = s.random(length=settings.OTP_LENGTH)

    return '{0}/{1}/{2}/{3}-{4}'.format('uploads', instance.vendor_slug, 'mobile_icon', rnd, filename)


class Currency(models.Model):
    class Meta:
        verbose_name = 'Currency'
        verbose_name_plural = 'Currencies'

    cr_code = models.CharField(max_length=3, unique=True, null=False, blank=False, verbose_name='Currency ISO Code')
    currency_name = models.CharField(max_length=25, null=False, blank=False)
    cr_prefix = models.CharField(null=True, max_length=5, blank=True, verbose_name="Currency Prefix")
    is_default = models.BooleanField(default=False, )
    status = models.BooleanField(u'Active', default=True)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.currency_name

    def __unicode__(self):
        return '{0}'.format(self.currency_name)


class PaymentVendor(models.Model):
    LOCAL_APPS = tuple([app_name, app_name] for app_name in settings.LOCAL_APPS)

    vendor_name = models.CharField(max_length=50)
    vendor_slug = models.SlugField(editable=False)
    server_address = models.CharField(max_length=100, verbose_name="Server URL", )
    server_timeout = models.IntegerField(default=5, verbose_name="Request Timeout (Seconds)")
    custom_rest_header = models.TextField(max_length=5000, null=True, blank=True )
    custom_params = models.TextField(max_length=5000, null=True, blank=True, verbose_name="Custom Attributes" )

    package = models.CharField(choices=LOCAL_APPS, max_length=50, null=True, blank=True)
    country = CountryField(
        verbose_name=_("country"), blank=True, null=True
    )
    icon = models.FileField(upload_to=mobile_icon_directory_path, null=True, blank=True, verbose_name="Mobile Icon")
    allow_server_request = models.BooleanField(default=False, verbose_name="Server Side Request")
    debug = models.BooleanField(default=False, verbose_name="Debug Controller")
    json_payload_format = models.TextField(max_length=12000, null=True, blank=True )
    status = models.BooleanField(default=True)

    def save(self):
        if not self.id:
            self.vendor_slug = slugify(self.vendor_name)
        if self.pk:
            self.transaction_id_regex = self.raw_transaction_id_regex
        super(BillingVendor, self).save()

    def __str__(self):
        return self.vendor_name

    class Meta:
        verbose_name = 'Payment Vendor'