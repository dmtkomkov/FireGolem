from django.conf.urls import url
from .views import BlogView

urlpatterns = [
    url(r'^$', BlogView.as_view(), name='home'),
]
