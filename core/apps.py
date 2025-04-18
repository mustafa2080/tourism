from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'
    verbose_name = _('Core')

    def ready(self):
        # Import translation options here to ensure they are registered
        # when the app is ready.
        import core.translation
