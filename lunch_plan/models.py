from django.db import models

from reference.models import BaseModel
from work_week.models import Day
from django.contrib.auth.models import User


class DailyPlan(BaseModel):
    user = models.ForeignKey(User)
    date = models.DateField()
    will_have_lunch = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.date}--{self.will_have_lunch}'

    def day(self):
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        return days[self.date.weekday()]
    day.short_description = "Day"


class WeeklyPlan(BaseModel):
    user = models.OneToOneField(User)
    office_lunch_days = models.ManyToManyField(Day)

    def __str__(self):
        return f'{self.user}'

    def admin_names(self):
        return ', '.join([a.name for a in self.office_lunch_days.all()])
    admin_names.short_description = "Office Lunch Days"
