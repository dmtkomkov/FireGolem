from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from .models import Post, Task, WorkLog, Label
from .paginator import CustomPagination
from .serializers import PostSerializer, TaskSerializer, UserSerializer, WorkLogSerializer, LabelSerializer

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


class TodoView(ModelViewSet):
    serializer_class = TaskSerializer
    queryset = Task.objects.all().order_by('-created_date')
    pagination_class = CustomPagination

    def perform_create(self, instance):
        instance.save(assignee=self.request.user)

    def perform_destroy(self, instance):
        instance.deleted = True
        instance.save()


class CurrentUserView(APIView):
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class WorkLogView(ModelViewSet):
    serializer_class = WorkLogSerializer
    queryset = WorkLog.objects.all().order_by('id')
    pagination_class = CustomPagination


class LabelView(ModelViewSet):
    serializer_class = LabelSerializer
    queryset = Label.objects.all().order_by('id')
    pagination_class = None
