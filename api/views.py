from blog.models import Post
from rest_framework import generics, mixins
from api.serializers import PostSerializer
from rest_framework.pagination import PageNumberPagination


class PostViewSet(generics.GenericAPIView,
                  mixins.ListModelMixin,
                  mixins.CreateModelMixin):
    queryset = Post.objects.all().order_by('date')
    serializer_class = PostSerializer
    pagination_class = PageNumberPagination

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
