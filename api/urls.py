from django.conf.urls import url
from rest_framework.routers import SimpleRouter

from .views import BlogView, CurrentUserView, GoalView, LabelView, LabelTableView, LabelGroupView

router = SimpleRouter(trailing_slash=False)
router.register("blog", BlogView)
router.register("goal", GoalView)
router.register("label", LabelView)
router.register("labelgroup", LabelGroupView)

urlpatterns = [
    url(r'^user$', CurrentUserView.as_view(), name='current_user'),
    url(r'^labelgroup$', LabelTableView.as_view(), name='label_table'),
]

urlpatterns += router.urls
