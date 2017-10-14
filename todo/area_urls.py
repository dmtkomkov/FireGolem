from django.conf.urls import url
from .views import AreaView

urlpatterns = [
    url(r'^$', AreaView.as_view(), name='home'),
]
