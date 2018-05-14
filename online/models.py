# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib import admin

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    created_time=models.DateField(auto_now_add=True)

    def __unicode__(self):
        return self.username


class Useradmin(admin.ModelAdmin):
    list_display = ('username','password','created_time')

# class Userlogin(admin.ModelAdmin):
#     list_display = ('username','login_time')

admin.site.register(User,Useradmin)