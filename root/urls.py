from django.conf.urls import url
from django.contrib.auth.views import LoginView, LogoutView
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework_jwt.views import refresh_jwt_token
from .views import RootView

app_name = 'root'

urlpatterns = [
    url(r'^$', RootView.as_view(), name='home'),
    url(r'^auth$', obtain_jwt_token, name='auth'),
    url(r'^refresh$', refresh_jwt_token, name='refresh'),
    url(r'^login$', LoginView.as_view(template_name='root/login.html'), {'extra_context': {'title': 'Login'}},
        name='login'),
    url(r'^logout$', LogoutView.as_view(), {'next_page': '/login'}, name='logout'),
]
