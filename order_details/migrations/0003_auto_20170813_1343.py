# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-08-13 07:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order_details', '0002_auto_20170812_2322'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='created_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='updated_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]