from django.contrib import admin
from django.db import models
from django.apps import apps
from .models import ProductModel, Product, BaseProductModel, Comment, CommentEditHistory, Ratings, Tag, Bookmarks, UnitPrice
from rangefilter.filters import DateRangeFilter, DateTimeRangeFilter
from import_export.admin import ImportExportActionModelAdmin


# models = apps.all_models['web_store'].values()

# for model in models:
# 	try:
# 		admclass = type(model._meta.model.__name__+'Admin', (admin.ModelAdmin,), {'list_display':tuple(map(lambda obj: obj.name,model._meta.fields))[1:]})
# 		admin.site.register(model,admclass)
# 	except admin.sites.AlreadyRegistered:
# 		pass
# 	except Exception as msg:
# 		print(msg)

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('tag', 'slug',  )
    search_fields = ('tag',)



@admin.register(UnitPrice)
class UnitPriceModelAdmin(ImportExportActionModelAdmin):
    list_display = ("unit_name", "init_length", "init_width", "final_length", "final_width", "currency", "price", "to_price", "price_type")
    search_fields =("init_length", "init_width", "final_length", "final_width")
    list_filter = ["unit_name", "price_type"]


@admin.register(BaseProductModel)
class BaseProductModelAdmin(admin.ModelAdmin):
    list_display = ('base_name', 'base_slug' )
    search_fields = ('base_name', )
    readonly_fields = ('base_slug', )
                   



@admin.register(ProductModel)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ('base_model', 'name', 'color', 'unit_price', 'is_draft', 'created_at' )
    search_fields = ('name','unit_price__unit_name' )
    autocomplete_fields = ['unit_price','base_model']
    list_filter = [ ('created_at', DateTimeRangeFilter),
                   ('updated_at', DateTimeRangeFilter), 'base_model' ]
    readonly_fields = ('model_slug', )
                   

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'unit_price', 'model', 'is_draft', 'description',)
    search_fields = ('name', 'unit_price__unit_name' )
    autocomplete_fields = ['tags',]
    list_filter = [ ('created_at', DateTimeRangeFilter),
                   ('updated_at', DateTimeRangeFilter), 'model' ]
    readonly_fields = ('product_slug', )

    
