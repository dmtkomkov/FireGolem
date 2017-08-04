from django.conf.urls import url
from . import views

# TODO: add Class for get and post
urlpatterns = [
    url(r'^$', views.index, name='blog'),
    url(r'^post/$', views.post, name='post')
]
