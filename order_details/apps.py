from django.apps import AppConfig


class OrderDetailsConfig(AppConfig):
    name = 'order_details'

    def ready(self):
        from order_details.signals import post_save_order, user_change_save
