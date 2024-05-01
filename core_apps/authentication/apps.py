from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ProfilesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "core_apps.authentication"
    verbose_name = _("Authentication")

    def ready(self):
        from core_apps.authentication import signals