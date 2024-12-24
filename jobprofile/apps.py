from django.apps import AppConfig


class JobProfileConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'jobprofile'

    def ready(self):
        import jobprofile.signals


