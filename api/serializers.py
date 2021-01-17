from rest_framework.serializers import ModelSerializer, SlugRelatedField

from django.contrib.auth.models import User
from api.models import Task, Post, UserIcon, WorkLog, Label, LabelGroup


class UserIconSerializer(ModelSerializer):
    class Meta:
        model = UserIcon
        fields = ('icon',)


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')


class ShortUserSerializer(ModelSerializer):
    user_icon = SlugRelatedField(read_only=True, slug_field='icon')

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'user_icon')


class PostSerializer(ModelSerializer):
    user = ShortUserSerializer(read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'title', 'body', 'created', 'user')


class TaskSerializer(ModelSerializer):
    assignee = ShortUserSerializer(read_only=True)

    class Meta:
        model = Task
        fields = ('id', 'name', 'assignee', 'created_date', 'completed_date')


class WorkLogSerializer(ModelSerializer):
    class Meta:
        model = WorkLog
        fields = ('log',)


class LabelGroupSerializer(ModelSerializer):
    class Meta:
        model = LabelGroup
        fields = ('name', 'single')


class LabelSerializer(ModelSerializer):
    group = LabelGroupSerializer()

    class Meta:
        model = Label
        fields = ('name', 'group')

    def create(self, label_data):
        group_data = label_data.pop('group')
        group = LabelGroup.objects.create(**group_data)
        label = Label.objects.create(group=group, **label_data)
        return label

