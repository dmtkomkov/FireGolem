from rest_framework.viewsets import ModelViewSet

from api.models import Post
from api.paginator import CustomPagination
from api.serializers import PostSerializer


class BlogView(ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all().order_by('-created')
    pagination_class = CustomPagination

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        instance.deleted = True
        instance.save()
