from django.contrib import admin
from django.db import models
from django.apps import apps
from .models import Profile
from rangefilter.filters import DateRangeFilter, DateTimeRangeFilter

    
    
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio', 'interests',)
    search_fields = ('user', 'bio', 'interests',)
    autocomplete_fields = ['favorites','follows']
    list_filter = [ ('created_at', DateTimeRangeFilter),
                   ('updated_at', DateTimeRangeFilter) ]
