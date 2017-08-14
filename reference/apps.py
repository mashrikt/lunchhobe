from django.apps import AppConfig


class ReferenceConfig(AppConfig):
    name = 'reference'

    def ready(self):
        from .signals import save_profile
