from django.contrib import admin
from django.db import models
from django.apps import apps
from .models import Currency
from rangefilter.filters import DateRangeFilter, DateTimeRangeFilter
from import_export.admin import ImportExportActionModelAdmin

# models = apps.all_models['common'].values()

# for model in models:
# 	try:
# 		admclass = type(model._meta.model.__name__+'Admin', (admin.ModelAdmin,), {'list_display':tuple(map(lambda obj: obj.name,model._meta.fields))[1:]})
# 		admin.site.register(model,admclass)
# 	except admin.sites.AlreadyRegistered:
# 		pass
# 	except Exception as msg:
# 		print(msg)




@admin.register(Currency)
class CurrencyModelAdmin(ImportExportActionModelAdmin):
    list_display = ("cr_code", "currency_name", "is_default",)
    search_fields =("cr_code","currency_name")



