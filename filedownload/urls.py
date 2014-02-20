# encoding: utf-8
from django.conf.urls import patterns, url
from filedownload.views import listMediaDir_view, DirectoryFileListView

urlpatterns = patterns('',
    #url(r'^login/$', login_view, name='login'),
    #url(r'^logout/$', logout_view, name='logout'),
    url(r'^$', listMediaDir_view , name='download-view'),
    url(r'^view/$', DirectoryFileListView.as_view() , name='files-view'),
)
