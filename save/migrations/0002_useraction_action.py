# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-05-17 11:08
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('save', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='useraction',
            name='action',
            field=models.CharField(default=django.utils.timezone.now, max_length=200),
            preserve_default=False,
        ),
    ]
