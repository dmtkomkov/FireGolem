from django.conf.urls import url
from django.contrib.auth import views as auth_views
from rest_framework_jwt.views import obtain_jwt_token
from . import views as home_views

urlpatterns = [
    url(r'^$', home_views.index, name='home'),
    url(r'^auth/$', obtain_jwt_token, name='auth'),
    url(r'^login/$', auth_views.login, {'template_name': 'home/login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/login'}, name='logout'),
]
