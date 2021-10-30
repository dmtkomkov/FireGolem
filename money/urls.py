from django.conf.urls import url
from .views import MoneyView, MoneyViewReport, MoneyViewGraph

app_name = 'money'

urlpatterns = [
    url(r'^$', MoneyView.as_view(), name='home'),
    url(r'^report/', MoneyViewReport.as_view(), name='report'),
    url(r'^graph/', MoneyViewGraph.as_view(), name='graph'),
]
