# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
from django.shortcuts import render,render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from django.template import RequestContext
from django import forms
from online.models import  User,Userlogin


#表单
#@csrf_protect
class UserFormLogin(forms.Form):
    username = forms.CharField(label='用户名',max_length=100)
    password = forms.CharField(label='密码',widget=forms.PasswordInput())

class UserForm(forms.Form):
    username = forms.CharField(label='用户名',max_length=100)
    password1 = forms.CharField(label='密码',widget=forms.PasswordInput())
    password2 = forms.CharField(label='确认密码',widget=forms.PasswordInput())
    email = forms.EmailField(label='电子邮件')


#注册
def regist(req):
    if req.method == 'POST':
        uf = UserForm(req.POST)
        if uf.is_valid():
            #获得表单数据
            username = uf.cleaned_data['username']
            password1 = uf.cleaned_data['password1']
            password2 = uf.cleaned_data['password2']
            email = forms.EmailField(label='邮箱')

            #添加到数据库
            if password1==password2:
               User.objects.create(username= username,password=password1)
            else: return HttpResponse("注册失败")
            return render_to_response('share.html')
    else:
        uf = UserForm()
    return render_to_response('regist.html',{'uf':uf},)
    #return render('regist.html',{'uf':uf},)

#登陆
def login(req):
    if req.method == 'POST':
        uf = UserFormLogin(req.POST)
        if uf.is_valid():
            #获取表单用户密码
            username = uf.cleaned_data['username']
            password = uf.cleaned_data['password']
            #获取的表单数据与数据库进行比较
            user = User.objects.filter(username__exact = username,password__exact = password)
            if user:
                #比较成功，跳转index
                response = HttpResponseRedirect('/online/index/')
                #将username写入浏览器cookie,失效时间为3600
                response.set_cookie('username',username,3600)
                Userlogin.objects.create(username= username)
                return response
            else:
                #比较失败，还在login
                return HttpResponseRedirect('/online/login/')
                 #return render_to_response('login.html',{"errors":"用户名已存在"})
    else:

        uf = UserFormLogin()
    return render_to_response('login.html',{'uf':uf},)

#登陆成功
def index(req):
    username = req.COOKIES.get('username','level')
    return render_to_response('index.html' ,{'username':username})


#退出
def logout(req):
    response = HttpResponse('logout !!')
    #清理cookie里保存username
    response.delete_cookie('username')
    return render_to_response('login.html',{"logout"})