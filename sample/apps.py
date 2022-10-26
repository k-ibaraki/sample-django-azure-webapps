from django.apps import AppConfig


class SampleConfig(AppConfig):
    default_auto_field: str = 'django.db.models.BigAutoField'
    name: str = 'sample'
