from django.conf.urls import url, include
from django.contrib import admin


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/v1/', include('api.urls', namespace='api')),
    url(r'^', include('root.urls', namespace='root')),
    url(r'^blog/', include('blog.urls', namespace='blog')),
    url(r'^money/', include('money.urls', namespace='money')),
]
