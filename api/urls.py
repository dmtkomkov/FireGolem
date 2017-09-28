from django.conf.urls import url
from api import views

urlpatterns = [
    url(r'^blog/', views.PostList.as_view(), name='blog'),
]
