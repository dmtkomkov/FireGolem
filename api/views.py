from blog.models import Post
from rest_framework.versioning import URLPathVersioning
from rest_framework import generics, mixins
from .serializers import PostSerializer, PostSerializer2
from .paginator import CustomPagination


class PostList(generics.GenericAPIView,
                  mixins.ListModelMixin,
                  mixins.CreateModelMixin):

    versioning_class = URLPathVersioning
    queryset = Post.objects.all().order_by('date')
    pagination_class = CustomPagination

    def get_serializer_class(self):
        if self.request.version == 'v1':
            return PostSerializer
        return PostSerializer2

    def get(self, request, *args, **kwargs):
        page_size = request.GET.get('page_size')           # Get custom page size from request params
        if page_size:
            self.pagination_class.page_size = page_size    # Set custom page size for paginator
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
