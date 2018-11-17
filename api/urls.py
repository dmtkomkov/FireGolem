from django.conf.urls import url
from api import views


urlpatterns = [
    url(r'^user/$', views.CurrentUserView.as_view(), name='current_user'),
    url(r'^blog/$', views.BlogView.as_view(), name='blog'),
    url(r'^blog/(?P<pk>\d+)/$', views.PostView.as_view(), name='post_update'),
]
