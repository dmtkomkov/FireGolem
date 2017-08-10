from blog.models import Post
from rest_framework import generics, mixins
from .serializers import PostSerializer
from .paginator import CustomPagination


class PostList(generics.GenericAPIView,
                  mixins.ListModelMixin,
                  mixins.CreateModelMixin):
    queryset = Post.objects.all().order_by('date')
    serializer_class = PostSerializer
    pagination_class = CustomPagination

    def get(self, request, *args, **kwargs):
        page_size = request.GET.get('page_size')           # Get custom page size from request params
        if page_size:
            self.pagination_class.page_size = page_size    # Set custom page size for paginator
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
