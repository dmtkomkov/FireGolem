from rest_framework.relations import SlugRelatedField
from rest_framework.serializers import ModelSerializer

from api.models import LabelGroup, Label, WorkLog


class LabelGroupSerializer(ModelSerializer):
    class Meta:
        model = LabelGroup
        fields = ('name', 'color')


class LabelSerializer(ModelSerializer):
    group = SlugRelatedField(slug_field='name', queryset=LabelGroup.objects.all(), allow_null=True)

    class Meta:
        model = Label
        fields = ('name', 'group')

    def to_internal_value(self, label_data):
        # Create new group by name or use existed
        # Otherwise set group to None if its not specified
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
    labels = SlugRelatedField(slug_field='name', many=True, queryset=Label.objects.all())

    class Meta:
        model = WorkLog
        fields = ('log', 'labels', 'date')

    def to_internal_value(self, worklog_data):
        # Added 'labels' as empty list if there is not labels key
        if worklog_data.get('labels') is None:
            worklog_data['labels'] = []
        return super(WorkLogSerializer, self).to_internal_value(worklog_data)

    def create(self, worklog_data):
        labels = worklog_data.pop('labels')
        instance = WorkLog.objects.create(**worklog_data)

        for label in labels:
            instance.labels.add(label)

        return instance

    def update(self, instance, worklog_data):
        instance.log = worklog_data['log']
        instance.labels = worklog_data['labels']
        instance.date = worklog_data['date']
        instance.save()
        return instance
