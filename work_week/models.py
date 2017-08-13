from django.db import models


# Create your models here.
from reference.models import BaseModel


class Day(BaseModel):
    name = models.CharField(max_length=10)
    is_working_day = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['pk']
