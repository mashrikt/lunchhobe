from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    User.objects.filter(id=instance.id).update(is_staff=True)
    employee_group = Group.objects.filter(name='Employee')
    if employee_group:
        User.objects.get(id=instance.id).groups.add(employee_group.first())
