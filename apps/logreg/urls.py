from django.conf.urls import url
from . import views
# from django.contrib import admin

urlpatterns = [
    url(r'^$', views.index),
    url(r'^friends$', views.friends),
    url(r'^login$', views.login),
    url(r'^register$', views.register),
    url(r'^user/(?P<id>\d+)/$', views.user),
    url(r'^user/add/(?P<id>\d+)$', views.addfriend),
    url(r'^user/remove/(?P<id>\d+)$', views.removefriend),
    url(r'^logout$', views.logout)
]