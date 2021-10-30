from django.conf.urls import url
from .views import BlogView

app_name = 'blog'

urlpatterns = [
    url(r'^$', BlogView.as_view(), name='home'),
]
