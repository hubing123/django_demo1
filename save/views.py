# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os

from django.shortcuts import render

# Create your views here.
#-*-coding:utf-8-*-
from django.shortcuts import render_to_response
from django.http   import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from save.models import *
from online import  models
from django.http import FileResponse
import logging
import logging.config
import  sys
def getlevel(username):
    level1=models.User.objects.values('level').get(username=username)
    level2=level1.values()
    level=level2[0]
  #  logging.config.fileConfig('logging.conf')
    logging.basicConfig(level = logging.INFO,format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger('level is')

    logger.info(level)
    logger.info(level1)
    logger.info(level2)

    return level
# Create your views here.
@csrf_exempt
def hdfsfile(request,username):
    # level=getlevel(username)
    # logger.info(level)
    from save.actionhdfs import get_all_file
    #如果是用户提交查询
    if request.method=="POST":
        path = request.POST.get("filepath")
        #level=int(getlevel(username))
        a=3
        level=getlevel(username)
       # logging(level)
        if level==1:
            path="/1"
        elif level==2:
            path="/2"
        else:path="/3"
        if path == "/":
            root_more=0
        else:
            root_more=1
        error=0
        try:
            mess_list = get_all_file(path)
        except:
            error="路径不存在或者为文件!"
            mess_list=[]
        return render_to_response("save.html", {
            "mess_list": mess_list,
            "path_value":path,
            "error":error,
            "root_more":root_more,
             "name":username,
            "level":level,
        })
    #如果是url直接定位到该界面，默认返回/
    else:
        #level=int(getlevel(username))
        a=3
        level=getlevel(username)
        #logging(level.values())
        if level==1:
            path="/1"
        elif level==2:
            path="/2"
        else:
            path="/3"
       # path="/"
        mess_list = get_all_file(path)
        return render_to_response("save.html",{
            "mess_list":mess_list,
            "path_value":path,
            "root_more":0,
            "name":username,
        })

#直接点击目录名进行下一级的查看
@csrf_exempt
def file(request,username,path):
    from save.actionhdfs import get_all_file
    path = path[5:]
    if path=="":
        root_more=0
    else:
        root_more=1
    try:
        error=0
        mess_list = get_all_file(path)
    except:
        mess_list=[]
        error="路径不存在或者为文件!"
    return render_to_response("save.html", {
        "mess_list": mess_list,
        "path_value": path,
        "root_more":root_more,
        "error":error,
        "name":username,
    })

#详情
@csrf_exempt
def more(request,username,path):
    from save.actionhdfs import show_more,get_all_file
    path=path.split("=")[1]
    try:
        error=0
        mess_list = get_all_file(path)
    except:
        error="路径不存在或者为文件!"
        mess_list=[]
    more_mess = show_more(path)
    return render_to_response("save.html",{
        "error":error,
        "more":1,
        "name":username,
        "mess_list": mess_list,
        "path_value": path,
        "more_mess":more_mess,
    })
#删除目录
def delete(request,username,path):
    new_path = "/".join(path.split("/")[:-1])
    from save.actionhdfs import delete_path
    delete_path(path[5:])
    logging.basicConfig(level = logging.INFO,format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger('path is')

    logger.info(path)
    logger.warn(path[5:])
    os.system("hadoop fs -rm -r %s"%(path))
    delete_path(path)
    action1=""
    action1="delete  "+path
    Useraction.objects.create(username= username,action=action1)
    return file(request,username,new_path)

@csrf_exempt
#创建目录
def mkdir(request,username,path):
    name = request.POST.get("mkdir") #用户提交的名字
    mk_path = path[5:] + "/" + name  #用来创建文件夹的名字
    from save.actionhdfs import mkdir_path
    if(mkdir_path(mk_path)):       #创建文件夹
        a=1
    else:a=2
    action1=""
    action1="make dircetion  "+mk_path
    Useraction.objects.create(username= username,action=action1)
    #Useraction.objects.create(username= username,action="make dircetion"+mk_path)
    return file(request,username,path)

@csrf_exempt
#重命名文件
def rename(request,username,path):
    name = request.POST.get("rename")  # 用户提交的名字
    rn_path = "/".join(path.split("/")[:-1])[5:] + "/" + name  # 用来重命名文件夹的名字
    from save.actionhdfs import rename_path
    rename_path(path[5:],rn_path)  # 重命名文件夹
    action1=""
    action1="rename  "+path+"  as  "+rn_path
    Useraction.objects.create(username= username,action=action1)
    return HttpResponseRedirect("/save/file/%s/%s" % (username,"/".join(path.split("/")[:-1])) )

#下载文件
@csrf_exempt
def down(request,username,path):
    name = request.POST.get("download") #用户提交的下载路径
    file_path = path[5:]  #文件在hdfs上的目录
    from save.actionhdfs import down_file
    down_file(file_path,'/usr/hubingtest/')       #创建文件夹
    action1=""
    action1="download  "+file_path+" "+" to "+name
    Useraction.objects.create(username= username,action=action1)
    lenth=len(file_path)
    count=0
    string1=''
    for i in range(0,lenth) :
        if file_path[i]=='/':
            count+=1
        if  count==3:
            break
        i+=1
    for j in range(i,lenth):
         string1+=file_path[j]
         j+=1
    open_path='/usr/hubingtest'+string1
    file=open(open_path,'rb')
    # mm='/usr/hubingtest/胡兵model12321.py'.encode('utf-8').decode('ISO-8859-1')
    # file=open(mm,'rb')
    response =FileResponse(file)
    response['Content-Type']='application/octet-stream'
    response['Content-Disposition']='attachment;filename="{}"'.format(string1).encode('utf-8').decode('ISO-8859-1')
    return response
    #return file(request,username,"/".join(path.split("/")[:-1]) )


#上传文件
@csrf_exempt
def upload(request,username,path):
    name = request.POST.get("up")  # 用户提交的上传文件路径
    content =request.FILES.get("upload", None)
    if not content:
      return HttpResponse("没有上传内容")
    position = os.path.join('/usr/hubingtest',content.name)
    storage = open(position,'wb+')       #打开存储文件
    for chunk in content.chunks():       #分块写入文件
        storage.write(chunk)
    storage.close()                      #写入完成后关闭文件
    file_path = path[5:]  # 文件在hdfs上的目录
    name="/usr/hubingtest/"+content.name
    from save.actionhdfs import upload_file
    upload_file(file_path,name)       #创建文件夹
    action1=""
    action1="upload  "+file_path+name
    Useraction.objects.create(username= username,action=action1)
    #return HttpResponse("上传成功")      #返回客户端信息

    # file_path = path[5:]  # 文件在hdfs上的目录
    # from save.actionhdfs import upload_file
    # upload_file(file_path,name)       #创建文件夹
    # action1=""
    # action1="upload  "+file_path+name
    # Useraction.objects.create(username= username,action=action1)
    return file(request,username, path)

 # def read(request,username,path):
 #     print("如果不是目录显示该文件内容")
