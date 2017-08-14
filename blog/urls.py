from django.conf.urls import url
from .views import BlogView

# TODO: add Class for get and post
urlpatterns = [
    url(r'^$', BlogView.as_view(), name='home'),
]
