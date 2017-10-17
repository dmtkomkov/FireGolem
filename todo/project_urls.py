from django.conf.urls import url
from .views import ProjectView, ProjectDetails

urlpatterns = [
    url(r'^$', ProjectView.as_view(), name='home'),
    url(r'^(?P<project_id>(\d+))', ProjectDetails.as_view(), name='details'),
]
