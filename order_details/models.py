from django.db import models

from reference.models import BaseModel
from work_week.models import Day
from django.contrib.auth.models import User

from dirtyfields import DirtyFieldsMixin


class Order(BaseModel, DirtyFieldsMixin):
    ENABLE_M2M_CHECK = True

    day = models.ForeignKey(Day)
    date = models.DateField()
    user = models.ManyToManyField(User)
    extra_orders = models.PositiveSmallIntegerField(default=0)
    price = models.DecimalField(max_digits=7, decimal_places=2, default=85)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=85)
    menu = models.CharField(max_length=150, blank=True)

    def __str__(self):
        return f"{self.date}--{self.day}"

    def no_of_orders(self):
        Order.objects.filter(id=self.id).update(total=(self.user.count() * self.price) +
                                                      (self.extra_orders * self.price))
        return f'{self.user.count()}+{self.extra_orders}'
    no_of_orders.short_description = "No. of Orders"
