from django.conf.urls import url
from . import views
# from django.contrib import admin

urlpatterns = [
    url(r'^$', views.index),
    url(r'^success$', views.success),
    url(r'^login$', views.login),
    url(r'^register$', views.register)
]