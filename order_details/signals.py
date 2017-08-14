from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver

from order_details.models import Order


@receiver(post_save, sender=Order)
def post_save_order(sender, instance, created, **kwargs):
    previous_extra_orders = instance.get_dirty_fields().get('extra_orders')
    previous_price = instance.get_dirty_fields().get('price')

    if previous_extra_orders != instance.extra_orders \
            or previous_price != instance.price:
        instance.calculate_total()


@receiver(m2m_changed, sender=Order.user.through)
def order_user_changed(sender, instance, **kwargs):
    instance.calculate_total()

