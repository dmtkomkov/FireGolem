from django.conf.urls import url, include
from rest_framework.routers import SimpleRouter

from .views import BlogView, CurrentUserView

router = SimpleRouter()
router.register("blog", BlogView)

urlpatterns = [
    url(r'^user/$', CurrentUserView.as_view(), name='current_user'),
    url(r'^', include(router.urls, namespace='blog')),
]
