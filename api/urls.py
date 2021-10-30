from django.conf.urls import url
from rest_framework.routers import SimpleRouter
from api.views import BlogView, GoalView, LabelView, LabelGroupView, LabelTableView, CurrentUserView

router = SimpleRouter(trailing_slash=False)
router.register("blog", BlogView)
router.register("goal", GoalView)
router.register("label", LabelView)
router.register("labelgroup", LabelGroupView)

app_name = 'api'

urlpatterns = [
    url(r'^user$', CurrentUserView.as_view(), name='current_user'),
    url(r'^labelgroup$', LabelTableView.as_view(), name='label_table'),
]

urlpatterns += router.urls
