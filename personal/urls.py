from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views
from django.contrib import admin

urlpatterns = [
    url(r'^$', views.index),
    url(r'^login/$', auth_views.login, {'template_name': 'personal/login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/login'}, name='logout'),
]
