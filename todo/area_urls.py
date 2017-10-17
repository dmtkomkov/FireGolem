from django.conf.urls import url
from .views import AreaView, AreaDetails

urlpatterns = [
    url(r'^$', AreaView.as_view(), name='home'),
    url(r'^(?P<area_id>(\d+))', AreaDetails.as_view(), name='details'),
]
