from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver

from order_details.models import Order


@receiver(m2m_changed, sender=Order.user.through)
def user_change_save(sender, instance, action, **kwargs):
    # print("Here")
    if action == "post_add" or action == "post_remove":
        # print("Inside post_add action")
        instance.user_orders()


@receiver(post_save, sender=Order)
def post_save_order(sender, instance, created, **kwargs):

    previous_extra_orders = instance.get_dirty_fields().get('extra_orders')

    if previous_extra_orders is not None:
        # print("Change in extra orders")
        if not previous_extra_orders and instance.extra_orders:
            # print(instance.total)
            # print(instance.price * instance.extra_orders)
            # print(instance.total + (instance.price * instance.extra_orders))
            instance.total = (instance.price * instance.extra_orders) + instance.total
            Order.objects.filter(id=instance.id).update(total=instance.total, extra_orders=instance.extra_orders)

        elif previous_extra_orders and instance.extra_orders:
            # print(instance.total)
            # print(instance.price * previous_extra_orders)
            # print(instance.price * instance.extra_orders)
            # print(instance.total + (instance.price * instance.extra_orders) -
            #       (instance.price * previous_extra_orders))
            instance.total = (instance.total + (instance.price * instance.extra_orders) -
                              (instance.price * previous_extra_orders))
            Order.objects.filter(id=instance.id).update(total=instance.total, extra_orders=instance.extra_orders)
