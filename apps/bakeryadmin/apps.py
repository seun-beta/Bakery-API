from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class BakeryadminConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.bakeryadmin"
    verbose_name = _("Bakery Admin")
