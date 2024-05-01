from datetime import datetime
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.conf import settings
from django.utils.text import slugify
from mptt.models import MPTTModel, TreeForeignKey
# from notifications.signals import notify
from core_apps.authentication.models import User
from core_apps.profiles.models import Profile
from core_apps.web_store.notification_emails import SendEmail
from core_apps.authentication.models import User
from core_apps.common.models import Currency, PaymentVendor
from django_extensions.db.fields import json
import shortuuid
import uuid




def product_model_image_directory_path(instance, filename):
    s = shortuuid.ShortUUID(alphabet="0123456789")
    rnd = s.random(length=6)

    return f'models/images/{instance.base_model.base_slug}/{rnd}-{filename}'

def product_image_directory_path(instance, filename):
    s = shortuuid.ShortUUID(alphabet="0123456789")
    rnd = s.random(length=6)

    return f'products/images/{instance.user.id}/{rnd}-{filename}'


def receipt_image_directory_path(instance, filename):
    s = shortuuid.ShortUUID(alphabet="0123456789")
    rnd = s.random(length=6)

    return f'payments/images/{instance.group.id}/{rnd}-{filename}'

class TimestampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True



class UnitPrice(models.Model):
    PRICE_TYPES = (
        ("MODEL", "MODEL"),
        ("PRODUCT", "PRODUCT"),
    )
    unit_name = models.CharField(max_length=120, editable=False, verbose_name="Unit Name")
    price_type = models.CharField(choices=PRICE_TYPES, null=True, max_length=20)
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT,null=True,blank=True )
    length = models.IntegerField()
    width = models.IntegerField()
    area = models.IntegerField()
    price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Price")


    def __str__(self):
        return '{}X{} {} Price {}{}-{}'.format(self.length, self.width, self.unit_name, self.currency.cr_prefix, self.price, self.price_type)
    
    def __unicode__(self):
        return '{}X{} {} Price {}{}-{}'.format(self.length, self.width, self.unit_name, self.currency.cr_prefix, self.price, self.price_type)


class BaseProductModel(models.Model):
    base_name = models.CharField(max_length=120, verbose_name="Base Model Name")
    base_slug = models.SlugField() 

    def save(self, *args, **kwargs):
        if not self.pk:
            self.base_slug = slugify(self.base_name)
        super(BaseProductModel, self).save(*args, **kwargs)

    def __str__(self):
        return self.base_name
    
    def __unicode__(self):
        return self.base_name


class ProductModel(models.Model):
    """
    Bunch of product belongs to a specific Product Model
    """
    base_model = models.ForeignKey(BaseProductModel, on_delete=models.CASCADE, related_name="%(app_label)s_%(class)s_related")
    name = models.CharField(max_length=120, verbose_name="Model Name")
    model_slug = models.SlugField() 
    color = models.CharField(max_length=30)
    color_code = models.CharField(max_length=20, null=True, blank=True, verbose_name="Color Code")
    description = models.TextField()
    model_image = models.ImageField(null=True, blank=True, upload_to=product_model_image_directory_path, verbose_name="Model Image")
    unit_price = models.ForeignKey(UnitPrice, on_delete=models.CASCADE, related_name="%(app_label)s_%(class)s_related")
    is_draft = models.BooleanField(default=True, )
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return self.name
    
    def __unicode__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.pk:
            self.model_slug = slugify(self.name)
        super(ProductModel, self).save(*args, **kwargs)
    
    class Meta:
        verbose_name = 'Product Model'


class Product(models.Model):
    """
    Ongoing Post thread before publishing post
    """
    name = models.CharField(max_length=120, editable=False, verbose_name="Model Name")
    product_slug = models.SlugField() 
    description = models.TextField()
    model = models.ForeignKey(ProductModel, on_delete=models.CASCADE, related_name="%(app_label)s_%(class)s_related")
    unit_price = models.ForeignKey(UnitPrice, on_delete=models.CASCADE, related_name="%(app_label)s_%(class)s_related")
    product_image = models.ImageField(null=True, blank=True, upload_to=product_image_directory_path, verbose_name="Product Image")
    tags = models.ManyToManyField(
        'web_store.Tag', related_name='web_store_tags'
    )
    is_draft = models.BooleanField(default=True, )
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return self.name
    
    def __unicode__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.pk:
            self.product_slug = slugify(self.name)
        super(Product, self).save(*args, **kwargs)
    
    class Meta:
        verbose_name = 'Product'



class SaleOrder(models.Model):
    """
    Define Order placed by User with Product Item 
    """
    ORDER_TYPES = (
        ("D2C", "D2C"),
        ("B2B", "B2B"),
    )
    name = models.CharField(max_length=120, editable=False, verbose_name="Model Name")
    order_id = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    order_sr_id = models.CharField(max_length=20, verbose_name="Order ID", editable=False)
    total_price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Price")
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="saleorder_created_by_user")
    product = models.ManyToManyField(
        'web_store.Product', related_name='web_store_product_orders'
    )
    quantity = models.IntegerField(verbose_name="Product Quantity")
    payment_completed = models.BooleanField(default=True, verbose_name="Payment Completed")
    discount_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, editable=False, verbose_name="Discount Amount")
    discount = models.DecimalField(max_digits=4, decimal_places=2, editable=False, null=True, blank=True, verbose_name="Discount(%)")
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT,null=True,blank=True )
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return self.name
    
    def __unicode__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        super(SaleOrder, self).save(*args, **kwargs)
    
    class Meta:
        verbose_name = 'Sale Order'



class PaymentModel(models.Model):
    is_cleaned = False
    group = models.ForeignKey(SaleOrder, on_delete=models.CASCADE, )
    received_amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Received Amount")
    transaction_id = models.CharField(max_length=50, null=True, blank=True, verbose_name="Payment Transaction ID")
    payment_receipt = models.FileField(upload_to=receipt_image_directory_path, null=True, blank=True, verbose_name="Payment Receipt")
    currency = models.ForeignKey(Currency, blank=True, null=True, related_name="payment_currency", on_delete=models.PROTECT)
    payment_vendor = models.ForeignKey(PaymentVendor, blank=True, null=True, editable=False, verbose_name="Payment Vendor", on_delete=models.CASCADE)
    cash_payment = models.BooleanField(default=False, verbose_name="Accepted Cash Payment")
    created_on = models.DateTimeField(auto_now_add=True, editable=False)
    received_on = models.DateField(null=True, blank=True,)


    def clean(self):
        super(PaymentModel, self).clean()

    def save(self, *args, **kwargs):
        if not self.is_cleaned:
            self.full_clean()
        
        if not self.pk:
            payment_model_qs = PaymentModel.objects.filter(transaction_id=self.transaction_id, payment_vendor=self.payment_vendor)
            if payment_model_qs.exists():
                raise ValidationError("Sorry, Transaction ID must be unique.")

        super(PaymentModel, self).save(*args, **kwargs)

   

    def __str__(self):
        vendor_slug = self.payment_vendor.vendor_slug if self.payment_vendor else ''
        received_on = self.received_on.strftime(settings.DATE_DISPLAY_FORMAT) if self.received_on else ''
        return "{}{} received on {} - {}".format(self.group.currency.cr_prefix, self.received_amount, received_on, vendor_slug)

    def __unicode__(self):
        vendor_slug = self.payment_vendor.vendor_slug if self.payment_vendor else ''
        received_on = self.received_on.strftime(settings.DATE_DISPLAY_FORMAT) if self.received_on else ''
        return "{}{} received on {} -{}".format(self.group.currency.cr_prefix, self.received_amount, received_on, vendor_slug)

    class Meta:
        verbose_name = 'Payment'
        indexes = [
            models.Index(
                fields=[
                    'group', 'payment_vendor', 'transaction_id'
                ]
            ),
        ]



class Comment(MPTTModel,TimestampModel):
    """
    Defines the comments table for an product
    """
    body = models.TextField()
    comment_likes = models.ManyToManyField(User, related_name='comment_likes', blank=True)
    comment_dislikes = models.ManyToManyField(User, related_name='comment_dislikes', blank=True)
    parent = TreeForeignKey('self',related_name='reply_set',null=True ,on_delete=models.CASCADE)
    product = models.ForeignKey(
        'web_store.Product', related_name='comments', on_delete=models.CASCADE
    )

    author = models.ForeignKey(
        'profiles.Profile', related_name='comments', on_delete=models.CASCADE
    )


class CommentEditHistory(models.Model):
    """
    Define comment_edit_history table and functionality
    """
    body = models.TextField(null=False)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=False)


class Ratings(models.Model):
    """
    Defines the ratings fields for a rater
    """
    rater = models.ForeignKey(
        Profile, on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product,  on_delete=models.CASCADE, related_name="rating")
    counter = models.IntegerField(default=0)
    stars = models.IntegerField(null=False)


class Tag(TimestampModel):
    """This class defines the tag model"""

    tag = models.CharField(max_length=255)
    slug = models.SlugField(db_index=True, unique=True)

    def __str__(self):
        return '{}'.format(self.tag)
      
      
class Bookmarks(models.Model):
    """
    Defines the model used for storing bookmarked products
    """
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='bookmarked')
    date = models.DateTimeField(default=datetime.now, blank=True)        


def pre_save_product_receiver(sender, instance, *args, **kwargs):
    """
    Method uses a signal to add slug to an post before saving it
    A slug will always be unique
    """
    if instance.slug:
        return instance
    slug = slugify(instance.title)
    num = 1
    unique_slug = slug
    # loops until a unique slug is generated
    while Product.objects.filter(slug=unique_slug).exists():
        unique_slug = "%s-%s" % (slug, num)
        num += 1

    instance.slug = unique_slug
