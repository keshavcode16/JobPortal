from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class WebStoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "core_apps.web_store"
    verbose_name = _("web_stores")
