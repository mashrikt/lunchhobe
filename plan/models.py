from django.db import models
from django.contrib.auth.models import User


class Timestamp(models.Model):
    created_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    class Meta:
        abstract = True


class Plan(Timestamp):
    user = models.OneToOneField(User)
    type = models.IntegerField(choices=((1, "Once"), (2, "Repeat")))


class PlanDetails(Timestamp):
    plan = models.ForeignKey(Plan)
    end_time = models.TimeField()
    status = models.IntegerField(choices=((1, "Active"), (2, "Cancelled"), (3, "Done")))
    sunday = models.NullBooleanField(default=False)
    monday = models.NullBooleanField(default=False)
    tuesday = models.NullBooleanField(default=False)
    wednesday = models.NullBooleanField(default=False)
    thursday = models.NullBooleanField(default=False)
    friday = models.NullBooleanField(default=False)
    saturday = models.NullBooleanField(default=False)
