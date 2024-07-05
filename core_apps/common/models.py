from datetime import datetime
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.conf import settings
from django.utils.text import slugify
from django_extensions.db.fields import json
from django.utils.translation import gettext_lazy as _






class Qualification(models.Model):
    name = models.CharField(max_length=500)
    status = models.BooleanField(u'Status', default=True)
    slug = models.SlugField(editable=False)

    def __str__(self):
        return self.name
    
    def __unicode__(self):
        return self.name

    def get_no_of_jobposts(self):
        from core_apps.jobapp.models import JobPost
        return JobPost.objects.filter(qualification__in=[self])
    
    def save(self):
        self.slug = slugify(self.name)
        super(Qualification, self).save()




class Skill(models.Model):
    name = models.CharField(max_length=500)
    status = models.BooleanField(u'Status', default=True)
    slug = models.SlugField(editable=False)

    def __str__(self):
        return self.name
    
    def __unicode__(self):
        return self.name

    def get_job_url(self):
        job_url = "/" + str(self.slug) + "-jobs/"
        return job_url

    def get_no_of_jobposts(self):
        from core_apps.jobapp.models import JobPost
        return JobPost.objects.filter(skills__in=[self], status="Live")

    def get_no_of_jobposts_all(self):
        from core_apps.jobapp.models import JobPost
        return JobPost.objects.filter(skills__in=[self])
    
    def get_no_of_applicants(self):
        from core_apps.users.models import User
        return User.objects.filter(skills__skill=self)

    def get_meta_data(self):
        if self.meta:
            return json.dumps(self.meta)
        else:
            return ""
    
    def save(self):
        self.slug = slugify(self.name)
        super(Skill, self).save()