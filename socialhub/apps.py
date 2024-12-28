# socialhub/apps.py

from django.apps import AppConfig

class SocialhubConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'socialhub'

    def ready(self):
        import socialhub.signals  # This ensures signals are connected