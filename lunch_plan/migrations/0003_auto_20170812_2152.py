# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-08-12 21:52
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lunch_plan', '0002_dailyplan_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='weeklyplan',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
