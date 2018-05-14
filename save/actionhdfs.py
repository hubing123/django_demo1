from hdfs import *
# connect hdfs
def connect():
    client = Client("http://192.168.1.105:50070")
    return client
#将字典转化为类
def dict2obj(args):
    '把字典递归转化为类'
    class obj(object):
        def __init__(self, d):
            for a, b in d.items():
                if isinstance(b, (list, tuple)):
                    setattr(self, a, [obj(x) if isinstance(x, dict) else x for x in b])
                else:
                    setattr(self, a, obj(b) if isinstance(b, dict) else b)
    return obj(args)

#get all file
def get_all_file(path):
    client = connect()
    mess_list = []
    if path=="/":
        pass
    else:
        path=path+"/"
    child_list = client.list(path)
    for child in child_list:
        one_dic = client.status(path+child)
        filepath = path+child
        one_dic["path"]=filepath
        dict2obj(one_dic)
        mess_list.append(dict2obj(one_dic))
    return mess_list

#more
def show_more(path):
    client = connect()
    return client.status(path)
#delete
def delete_path(path):
    client = connect()
    return client.delete(path,recursive=True)

#makedirs
def mkdir_path(path):
    client = connect()
    return client.makedirs(path)

#重命名
def rename_path(old_path,new_path):
    client = connect()
    return client.rename(old_path,new_path)

#下载文件
def down_file(hdfs_path,local_path):
    client = connect()
    return client.download(hdfs_path,local_path,overwrite=True)

#上传文件
def upload_file(hdfs_path,local_path):
    client = connect()
    return client.upload(hdfs_path,local_path,overwrite=True)
