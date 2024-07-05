from datetime import datetime, timedelta

from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin, Group
)
from django.db import models, transaction
from django.db.transaction import atomic
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from core_apps.common.models import Skill, Qualification
from .verification import SendEmail, account_activation_token
from django.dispatch import receiver
from django.db.models.signals import post_save,post_delete
from .tasks import send_email_task






class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **kwargs):
        """Create and return a `User` with an email and password."""
        if email is None:
            raise TypeError('Users must have an email address.')

        user = self.model(email=self.normalize_email(email), **kwargs)
        user.set_password(password)
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
    username = models.CharField(max_length=255, db_index=True, unique=True)
    user_type = models.CharField(choices=settings.USER_TYPES, null=True, max_length=20)
    # checking if a new user has verified their account from the verification email
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # The `is_reset` flag is used to allow change of password if true
    is_reset = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    get_notified = models.BooleanField(default=True)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
    objects = UserManager()

    def __str__(self):
        return self.email
    
    def __unicode__(self):
        return f'{self.first_name} {self.last_name} ({self.email})'

    def get_full_name(self):
        """
        Returns a user's  full name
        """
        return ' '.join((self.first_name,self.last_name))

class UserGroup(Group):
    user_type = models.CharField(choices=settings.USER_TYPES, max_length=20, unique=True)
    user_prefix = models.CharField(max_length=20, verbose_name=u'User Prefix', )

    class Meta:
        verbose_name = 'Permission group'

    def __str__(self):
        return self.user_prefix

    def __unicode__(self):
        return '{0}'.format(self.user_prefix)


class Employer(User):
    company_name = models.CharField(max_length=255)
    user_type = "EMPLOYER"
    is_staff = False
    is_superuser = False

    class Meta:
        verbose_name = "Employer"

    def clean(self):
        try:
            if not self.company_name:
                raise ValidationError("Missing Company Name")
        except ValidationError as err:
            raise ValidationError("Opps! Unknown Error for Company Name Validation.", err)

        if not self.username:
            self.username = self.email
        super(Employer, self).clean()

    def save(self, *args, **kwargs):
        self.user_type = "EMPLOYER"

        self.is_staff = False
        self.is_superuser = False

        super(Employer, self).save(*args, **kwargs)
        
    def get_total_job_counts(self):
        from core_apps.jobapp.models import JobPost
        record_counts = JobPost.objects.filter(created_by=self).count()
        return record_counts
    
    def get_total_job_applicants(self):
        from core_apps.jobapp.models import JobApplication
        record_counts = JobApplication.objects.filter(job_post__created_by=self).count()
        return record_counts


class JobSeeker(User):
    user_type = "JOB_SEEKER"
    primary_skills = models.ManyToManyField(Skill, blank=True)
    higher_qualification = models.ForeignKey(Qualification, null=True, blank=True, on_delete=models.CASCADE)

    is_staff = False
    is_superuser = False

    class Meta:
        verbose_name = "Job Seeker"
        

    def clean(self):
        try:
           pass
        except ValidationError as err:
            raise ValidationError("Opps! Unknown Error for Phonenumber Validation.", err)

        super(JobSeeker, self).clean()

    def save(self, *args, **kwargs):
        self.user_type = "JOB_SEEKER"

        self.is_staff = False
        self.is_superuser = False

        super(JobSeeker, self).save(*args, **kwargs)



@receiver(post_save, sender=Employer, dispatch_uid="send_employer_mail_verification")
def send_employer_mail_verification(sender, instance, created, **kwargs):
    if created:
        if not instance.is_verified:
            send_email_task.delay(instance.email)

@receiver(post_save, sender=JobSeeker, dispatch_uid="send_user_mail_verification")
def send_user_mail_verification(sender, instance, created, **kwargs):
    if created:
        if not instance.is_verified:
            send_email_task.delay(instance.email)