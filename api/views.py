from rest_framework import generics, mixins
from rest_framework.versioning import URLPathVersioning

from api.models import Post
from .paginator import CustomPagination
from .serializers import PostSerializer


class PostList(generics.GenericAPIView,
                  mixins.ListModelMixin,
                  mixins.CreateModelMixin):

    serializer_class = PostSerializer
    versioning_class = URLPathVersioning
    queryset = Post.objects.all().order_by('created')
    pagination_class = CustomPagination

    def get(self, request, *args, **kwargs):
        page_size = request.GET.get('page_size')           # Get custom page size from request params
        if page_size:
            self.pagination_class.page_size = page_size    # Set custom page size for paginator
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
