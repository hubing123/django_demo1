# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-05-17 20:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('online', '0005_auto_20180514_1711'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='level',
            field=models.IntegerField(default=1),
        ),
    ]
