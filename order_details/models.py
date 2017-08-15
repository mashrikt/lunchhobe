from django.db import models

from order_details.config import DateWeekDay
from reference.models import BaseModel
from work_week.models import Day
from django.contrib.auth.models import User
from django.utils import timezone

from dirtyfields import DirtyFieldsMixin


class Order(BaseModel, DirtyFieldsMixin):
    day = models.ForeignKey(Day, blank=True, null=True)
    date = models.DateField(default=timezone.now)
    user = models.ManyToManyField(User, blank=True)
    extra_orders = models.PositiveSmallIntegerField(default=0)
    price = models.DecimalField(max_digits=7, decimal_places=2, default=85)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=85)
    menu = models.CharField(max_length=150, blank=True)

    def __str__(self):
        return f"{self.date}--{self.day}"

    def day_of_week(self):
        # return self.date.weekday()
        return f'{DateWeekDay.CHOICES[self.date.weekday()][1]}'
    day_of_week.short_description = "Day"

    def no_of_orders(self):
        return f'{self.user.count()}+{self.extra_orders}'
    no_of_orders.short_description = "No. of Orders"

    def calculate_total(self):
        Order.objects.filter(id=self.id).update(total=(self.user.count() + self.extra_orders) * self.price)
