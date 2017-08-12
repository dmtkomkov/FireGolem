from django.conf.urls import url, include

# TODO: add namespaces for different applications
urlpatterns = [
    url(r'^auth/', include('rest_auth.urls')),
    url(r'^api/', include('api.urls')),
    url(r'^', include('home.urls')),
    url(r'^blog/', include('blog.urls')),
]
