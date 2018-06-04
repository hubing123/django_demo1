# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib import admin
# Create your models here.
class Useraction(models.Model):
    username=models.CharField(max_length=50)
    actiontime=models.DateTimeField(auto_now=True)
    action=models.CharField(max_length=200)
    #int=models.IntegerField(default=0)

class actionadmin(admin.ModelAdmin):
    list_display = ('username','actiontime','action')


admin.site.register(Useraction,actionadmin)