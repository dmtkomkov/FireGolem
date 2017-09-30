from django.conf.urls import url
from .views import TodoView, TodoDetails

urlpatterns = [
    url(r'^$', TodoView.as_view(), name='home'),
    url(r'^(?P<task_id>(\d+))', TodoDetails.as_view(), name='details'),
]
