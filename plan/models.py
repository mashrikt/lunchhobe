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

    def __str__(self):
        return str(self.user) + " - " + str(self.type)


class Days(Timestamp):
    value = models.CharField(max_length=10)

    def __str__(self):
        return str(self.value)


class PlanDetails(Timestamp):
    plan = models.ForeignKey(Plan)
    end_time = models.TimeField()
    day = models.ManyToManyField(Days)
    status = models.IntegerField(choices=((1, "Active"), (2, "Cancelled"), (3, "Done")))

    def __str__(self):
        return str(self.plan.__str__()) + " - " + str(self.status)
