from django.db import models

from work_week.models import Day
from django.contrib.auth.models import User


class DailyPlan(models.Model):
    user = models.ForeignKey(User)
    day = models.ForeignKey(Day)
    date = models.DateField()
    will_have_lunch = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.day}-{self.date}--{self.will_have_lunch}'


class WeeklyPlan(models.Model):
    user = models.OneToOneField(User)
    office_lunch_days = models.ManyToManyField(Day)

    def __str__(self):
        return f'{self.user}'

    def admin_names(self):
        return ', '.join([a.name for a in self.office_lunch_days.all()])
    admin_names.short_description = "Office Lunch Days"
