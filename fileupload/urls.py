# encoding: utf-8
from django.conf.urls import patterns, url

from fileupload.views import (
        BasicVersionCreateView, BasicPlusVersionCreateView,
        jQueryVersionCreateView, AngularVersionCreateView,
        FileCreateView, FileDeleteView, FileListView,
        login_view, logout_view,
        )

urlpatterns = patterns('',
    url(r'^login/$', login_view, name='login'),
    url(r'^logout/$', logout_view, name='logout'),
    url(r'^home/$', jQueryVersionCreateView.as_view(), name='upload-jquery'),
    url(r'^delete/(?P<pk>\d+)$', FileDeleteView.as_view(), name='upload-delete'),
    url(r'^view/$', FileListView.as_view(), name='upload-view'),
)
