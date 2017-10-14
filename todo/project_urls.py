from django.conf.urls import url
from .views import ProjectView

urlpatterns = [
    url(r'^$', ProjectView.as_view(), name='home'),
]
