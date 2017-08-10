from django.conf.urls import url
from api import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    url(r'^(?P<version>(v1|v2))/blog/', views.PostList.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)