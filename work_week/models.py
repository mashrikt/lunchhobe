from django.db import models


# Create your models here.
class Day(models.Model):
    name = models.CharField(max_length=10)
    is_working_day = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['pk']
