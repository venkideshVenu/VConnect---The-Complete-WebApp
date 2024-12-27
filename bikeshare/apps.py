from django.apps import AppConfig

class BikeShareConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'bikeshare'

    def ready(self):
        import bikeshare.signals  # noqa