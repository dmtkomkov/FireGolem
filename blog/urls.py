from django.conf.urls import url
from . import views

# TODO: add Class for get and post
urlpatterns = [
    url(r'^$', views.index, name='home'),
    url(r'^post/$', views.post, name='post')
]
