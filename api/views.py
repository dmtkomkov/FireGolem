from blog.models import Post
from rest_framework import generics, mixins
from api.serializers import PostSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CustomPagination(PageNumberPagination):
    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,
            'page_size': self.page_size,
            'page_number': self.page.number,
            'page_count': self.page.paginator.num_pages,
            'results': data
        })


class PostList(generics.GenericAPIView,
                  mixins.ListModelMixin,
                  mixins.CreateModelMixin):
    queryset = Post.objects.all().order_by('date')
    serializer_class = PostSerializer
    pagination_class = CustomPagination

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
