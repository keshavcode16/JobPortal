from datetime import datetime, timedelta

from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin, Group
)
from django.db import models, transaction
from django.db.transaction import atomic
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField






class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **kwargs):
        """Create and return a `User` with an email and password."""
        if email is None:
            raise TypeError('Users must have an email address.')

        user = self.model(email=self.normalize_email(email), **kwargs)
        user.set_password(password)
        user.save()

        return user

    def create_user_from_google(self, email, firstname, lastname, google_user_id, **kwargs):
        user = self.model(email=email, **kwargs)
        user.first_name = firstname
        user.last_name = lastname
        user.is_verified = True
        user.meta = dict(google_user_id=google_user_id)
        user.save()
        return user

    def create_superuser(self,  email, password=None, **kwargs):
        if password is None:
            raise TypeError('Superusers must have a password.')
        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True
        user.is_verified = True
        user.save()

        return user



class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(db_index=True, unique=True)
    first_name = models.CharField(max_length=255, )
    last_name = models.CharField(max_length=255, null=True, default=None)
    username = models.CharField(max_length=255, null=True, blank=True)
    phone_number = PhoneNumberField(
        verbose_name=_("phone number"), max_length=30
    )
    user_role = models.CharField(choices=settings.USER_ROLES, null=True, max_length=20)
    country = CountryField(
        verbose_name=_("country"), blank=True, null=True
    )
    # checking if a new user has verified their account from the verification email
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # The `is_reset` flag is used to allow change of password if true
    is_reset = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    get_notified = models.BooleanField(default=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    objects = UserManager()

    def __str__(self):
        return self.email
    
    def __unicode__(self):
        return f'{self.first_name} {self.last_name} ({self.email})'

    def get_full_name(self):
        """
        Returns a user's  username
        """
        return ' '.join((self.first_name,self.last_name))

class UserGroup(Group):
    user_role = models.CharField(choices=settings.USER_ROLES, max_length=20, unique=True)
    user_prefix = models.CharField(max_length=20, verbose_name=u'User Prefix', )

    class Meta:
        verbose_name = 'Permission group'

    def __str__(self):
        return self.user_prefix

    def __unicode__(self):
        return '{0}'.format(self.user_prefix)


class Customer(User):
    date_of_birth = models.DateField(null=True, blank=True)
    marital_status = models.CharField(choices=settings.MARITAL_STATUS, max_length=50, null=True, blank=True, verbose_name= "Marital Status")
    user_type = "CUSTOMER"
    is_staff = False
    is_superuser = False

    class Meta:
        verbose_name = "Customer"

    def clean(self):
        try:
            if not self.cc_code:
                raise ValidationError("Missing Country")
        except ValidationError as err:
            raise ValidationError("Opps! Unknown Error for Phonenumber Validation.", err)

        if not self.username:
            self.username = self.email
        super(Customer, self).clean()

    def save(self, *args, **kwargs):
        self.user_type = "CUSTOMER"

        if not self.is_cleaned:
            self.full_clean()

        if self.pk is None:
            getUserGroup = UserGroup.objects.get(user_type=self.user_type) 
            re_count = Customer.objects.filter(user_type=self.user_type).count()

            if getUserGroup:
                if re_count == 0:
                    self.username = 1
                else:
                    self.username = (re_count + 100)

                self.username = "{}{}".format(getUserGroup.uid_prefix, self.username)

        self.is_staff = False
        self.is_superuser = False

        super(Customer, self).save(*args, **kwargs)