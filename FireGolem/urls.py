from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/v1/', include('api.urls', namespace='api')),
    url(r'^', include('root.urls', namespace='root')),
    url(r'^blog/', include('blog.urls', namespace='blog')),
    url(r'^todo/', include('todo.urls', namespace='todo')),
    url(r'^area/', include('todo.area_urls', namespace='area')),
    url(r'^project/', include('todo.project_urls', namespace='project')),
]
