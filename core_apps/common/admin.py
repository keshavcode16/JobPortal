from django.contrib import admin
from django.db import models
from django.apps import apps
from .models import Skill, Qualification
from rangefilter.filters import DateRangeFilter, DateTimeRangeFilter
from import_export.admin import ImportExportActionModelAdmin




@admin.register(Skill)
class SkillModelAdmin(ImportExportActionModelAdmin):
    list_display = ("name", "status", )
    search_fields =("name",)


@admin.register(Qualification)
class QualificationModelAdmin(ImportExportActionModelAdmin):
    list_display = ("name", "status", )
    search_fields =("name",)
