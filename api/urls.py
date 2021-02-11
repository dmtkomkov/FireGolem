from django.conf.urls import url
from rest_framework.routers import SimpleRouter

from .views import BlogView, TodoView, CurrentUserView, WorkLogView, LabelView, LabelGroupView

router = SimpleRouter(trailing_slash=False)
router.register("blog", BlogView)
router.register("todo", TodoView)
router.register("worklog", WorkLogView)
router.register("label", LabelView)

urlpatterns = [
    url(r'^user$', CurrentUserView.as_view(), name='current_user'),
    url(r'^labelgroup$', LabelGroupView.as_view(), name='label_group'),
]

urlpatterns += router.urls
