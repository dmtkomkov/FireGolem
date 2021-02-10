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


class LabelGroupSerializer(ModelSerializer):
    class Meta:
        model = LabelGroup
        fields = ('name', 'single')


class LabelSerializer(ModelSerializer):
    group = SlugRelatedField(slug_field='name', queryset=LabelGroup.objects.all(), allow_null=True)

    class Meta:
        model = Label
        fields = ('name', 'group')

    def to_internal_value(self, label_data):
        # Create new group by name
        # Otherwise set group to None
        if label_data.get('group'):
            LabelGroup.objects.get_or_create(name=label_data['group'])
        else:
            label_data['group'] = None
        return super(LabelSerializer, self).to_internal_value(label_data)

    def create(self, label_data):
        instance = Label.objects.create(**label_data)
        return instance

    def update(self, instance, label_data):
        instance.name = label_data['name']
        instance.group = label_data['group']
        instance.save()
        return instance


class WorkLogSerializer(ModelSerializer):
    labels = LabelSerializer(many=True)

    class Meta:
        model = WorkLog
        fields = ('log', 'labels')

    def create(self, worklog_data):
        labels_data = worklog_data.pop('labels')
        instance = WorkLog.objects.create(**worklog_data)

        for label_data in labels_data:
            label = Label.objects.get(name=label_data["name"])
            instance.labels.add(label)

        return instance
