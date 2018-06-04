# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib import admin

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    level=models.IntegerField(default=1)
    created_time=models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.username

class Userlogin(models.Model):
   username=models.CharField(max_length=50)
   logintime=models.DateTimeField(auto_now=True)


class Useradmin(admin.ModelAdmin):
    list_display = ('username','password','created_time',"level")


class loginadmin(admin.ModelAdmin):
  list_display = ('username','logintime')


admin.site.register(User,Useradmin)
admin.site.register(Userlogin,loginadmin)