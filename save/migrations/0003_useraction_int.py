# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-05-17 20:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('save', '0002_useraction_action'),
    ]

    operations = [
        migrations.AddField(
            model_name='useraction',
            name='int',
            field=models.IntegerField(default=0),
        ),
    ]