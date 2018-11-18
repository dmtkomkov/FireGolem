from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from .models import Post
from .paginator import CustomPagination
from .serializers import PostSerializer, UserSerializer

from rest_framework.response import Response


class BlogView(ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all().order_by('-created')
    pagination_class = CustomPagination

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        instance.deleted = True
        instance.save()

class CurrentUserView(APIView):

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
