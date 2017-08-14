from django.conf.urls import url, include
from django.contrib import admin

# TODO: add namespaces for different applications
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include('api.urls')),
    url(r'^', include('home.urls')),
    url(r'^blog/', include('blog.urls')),
]
