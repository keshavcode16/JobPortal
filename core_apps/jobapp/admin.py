from django.contrib import admin
from django.db import models
from django.apps import apps
from .models import JobPost, JobApplication
from rangefilter.filters import DateRangeFilter, DateTimeRangeFilter
from import_export.admin import ImportExportActionModelAdmin




@admin.register(JobPost)
class JobPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'status', 'created_on' )
    search_fields = ('title', )
    autocomplete_fields = ['skills','created_by']
    list_filter = [ ('created_on', DateTimeRangeFilter),
                   ('modified_on', DateTimeRangeFilter), ]
    readonly_fields = ('created_by', 'qualification')


@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ('job_post', 'user',  'status', 'applied_on' )
    search_fields = ('job_post__name', 'user' )
    autocomplete_fields = ['job_post',]
    list_filter = [ ('applied_on', DateTimeRangeFilter), ]
    readonly_fields = ('job_post', 'user')



                   



                   
    
