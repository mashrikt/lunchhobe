from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save
from django.dispatch import receiver

from lunch_plan.models import WeeklyPlan


@receiver(post_save, sender=User)
def save_profile(sender, instance, created, **kwargs):
    if created:
        WeeklyPlan.objects.create(user=instance)
    User.objects.filter(id=instance.id).update(is_staff=True)
    employee_group = Group.objects.filter(name='Employee')
    if employee_group:
        User.objects.get(id=instance.id).groups.add(employee_group.first())
