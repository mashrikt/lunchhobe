from django.apps import AppConfig


class OrderDetailsConfig(AppConfig):
    name = 'order_details'
    icon = '<i class="material-icons">assignment</i>'

    def ready(self):
        from order_details.signals import post_save_order
