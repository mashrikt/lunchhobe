from django.db.models.signals import post_save
from django.dispatch import receiver

from order_details.models import Order


@receiver(post_save, sender=Order)
def post_save_order(sender, instance, created, **kwargs):

    previous_extra_orders = instance.get_dirty_fields().get('extra_orders')

    if not previous_extra_orders and instance.extra_orders != 0:
        instance.total = (instance.price * instance.extra_orders) + instance.total
        instance.save()

    elif previous_extra_orders and instance.extra_orders != 0:
        instance.total = (instance.total -
                          (instance.price * previous_extra_orders) +
                          (instance.price * instance.extra_orders))
        instance.save()
