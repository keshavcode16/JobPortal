from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from .models import User, UserGroup
from import_export import fields, resources, widgets
from import_export.admin import ImportExportActionModelAdmin, ImportExportModelAdmin
import django
from django.utils.encoding import smart_str
django.utils.encoding.smart_text = smart_str
# from django.apps import apps
# models = apps.all_models['authentication'].values()

# for model in models:
# 	try:
# 		admclass = type(model._meta.model.__name__+'Admin', (admin.ModelAdmin,), {'list_display':tuple(map(lambda obj: obj.name,model._meta.fields))[1:]})
# 		admin.site.register(model,admclass)
# 	except admin.sites.AlreadyRegistered:
# 		pass
# 	except Exception as msg:
# 		print(msg)

class UserGroupModelResource(resources.ModelResource):
    class Meta:
        model = UserGroup
        fields = ('id', 'name' ,'user_role','user_prefix', 'permissions' )
        export_order = ('id', 'name' ,'user_role','user_prefix', 'permissions' )


@admin.register(UserGroup)
class UserGroupAdmin(ImportExportModelAdmin):
    resource_class = UserGroupModelResource
    list_display = ('user_role', 'user_prefix',  )


@admin.register(User)
class UserAdmin(ImportExportModelAdmin):
    list_display = ["username", "first_name", "last_name", "email","is_staff", "password"]
    search_fields = ["username", "first_name", "last_name", "email"]
   
    def has_add_permission(self, request, obj=None):
        return True

    def has_change_permission(self, request, obj=None):
        # if obj and obj.user_role != None:
        #     return False
        # return super(UserAdmin, self).has_change_permission(request, obj)
        return True

    def has_delete_permission(self, request, obj=None):
        return True