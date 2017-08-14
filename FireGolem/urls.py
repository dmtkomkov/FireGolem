from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include('api.urls', namespace='api')),
    url(r'^', include('home.urls', namespace='root')),
    url(r'^blog/', include('blog.urls', namespace='blog')),
]
