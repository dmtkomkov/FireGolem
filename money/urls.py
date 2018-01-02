from django.conf.urls import url
from .views import MoneyView

urlpatterns = [
    url(r'^$', MoneyView.as_view(), name='home'),
]
