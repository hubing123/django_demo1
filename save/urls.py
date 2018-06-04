from django.conf.urls import url

from save.views import *

urlpatterns = [
    url(r'^hdfsfile/(\w+)/$', hdfsfile),
    url(r'^more/(\w+)/(.+)/$', more),
    url(r'^file/(\w+)/(.+)/$', file),
    url(r'^delete/(\w+)/(.+)/$', delete),
    url(r'^mkdir/(\w+)/(.+)/$', mkdir),
    url(r'^rename/(\w+)/(.+)/$', rename),
    url(r'^down/(\w+)/(.+)/$', down),
    url(r'^upload/(\w+)/(.+)/$', upload),
    #url(r'^hdfsfile$', hdfsfile),
]
