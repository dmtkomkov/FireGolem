from collections import defaultdict

from rest_framework.mixins import UpdateModelMixin
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.response import Response

from .models import Post, WorkLog, Label, LabelGroup
from .paginator import CustomPagination
from .serializers import PostSerializer, UserSerializer, WorkLogSerializer, LabelSerializer, \
    LabelGroupSerializer


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


class GoalView(ModelViewSet):
    serializer_class = WorkLogSerializer
    queryset = WorkLog.objects.all().order_by('id')
    pagination_class = CustomPagination


class LabelView(ModelViewSet):
    serializer_class = LabelSerializer
    queryset = Label.objects.all().order_by('id')
    pagination_class = None

    def perform_destroy(self, instance):
        # Remove group if it contains no labels
        group = instance.group
        instance.delete()
        if group.labels.count() == 0:
            group.delete()


class LabelGroupView(UpdateModelMixin, GenericViewSet):
    serializer_class = LabelGroupSerializer
    queryset = LabelGroup.objects.all().order_by('id')
    pagination_class = None


class LabelTableView(APIView):
    def get(self, request):
        # outer join for label group to include NO_GROUP category
        labels = list(Label.objects.all().values('name', 'group__name'))
        result = defaultdict(list)
        for label in labels:
            key = label['group__name'] or 'NO_GROUP'
            result[key].append(label['name'])
        return Response(result)
