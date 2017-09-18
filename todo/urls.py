from django.conf.urls import url
from .views import TodoView

urlpatterns = [
    url(r'^$', TodoView.as_view(), name='home'),
]
