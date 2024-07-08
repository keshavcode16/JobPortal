from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class JobAppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "core_apps.jobapp"
    verbose_name = _("jobapp")
