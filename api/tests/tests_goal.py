from datetime import date

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from api.models import LabelGroup, Label, WorkLog


class LabelTests(APITestCase):
    username = 'tester'
    password = 'tester_password'

    def setUp(self):
        test_user = User.objects.create_user(username=self.username, password=self.password)
        self.client.force_authenticate(user=test_user)
        self.label_name = 'My label'
        self.group_name = 'My group'

    def test_create_label_with_new_group(self):
        # init
        label = {'name': self.label_name, 'group': self.group_name}
        url = reverse('api:label-list')
        # action
        response = self.client.post(url, label, format='json')
        # check
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.check_label()

    def test_create_label_with_existed_group(self):
        # init
        label = {'name': self.label_name, 'group': self.group_name}
        url = reverse('api:label-list')
        LabelGroup.objects.create(name=self.group_name)
        # action
        response = self.client.post(url, label, format='json')
        # check
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.check_label()

    def test_create_label_without_group(self):
        # init
        label = {'name': self.label_name}
        url = reverse('api:label-list')
        # action
        response = self.client.post(url, label, format='json')
        # check
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Label.objects.count(), 1)
        self.assertEqual(LabelGroup.objects.count(), 0)
        db_label = Label.objects.first()
        self.assertEqual(db_label.name, self.label_name)
        self.assertEqual(db_label.group, None)

    def test_update_label(self):
        # init
        label = {'name': self.label_name, 'group': self.group_name}
        url = reverse('api:label-detail', args=[1])
        new_label = {'name': 'New label'}
        group = LabelGroup.objects.create(name=self.group_name)
        Label.objects.create(name=self.label_name, group=group)
        # action
        response = self.client.put(url, new_label, format='json')
        # check
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Label.objects.count(), 1)
        self.assertEqual(LabelGroup.objects.count(), 1)
        db_label = Label.objects.first()
        self.assertEqual(db_label.name, 'New label')
        self.assertEqual(db_label.group, None)
        # action
        response = self.client.put(url, label, format='json')
        # check
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        db_label = Label.objects.first()
        self.assertEqual(db_label.name, self.label_name)
        self.assertEqual(db_label.group.name, self.group_name)

    def test_delete_label(self):
        # init
        group = LabelGroup.objects.create(name=self.group_name)
        Label.objects.create(name=self.label_name, group=group)
        Label.objects.create(name='additional label', group=group)
        url = reverse('api:label-detail', args=[1])
        # action
        response = self.client.delete(url, format='json')
        # check
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Label.objects.count(), 1)
        self.assertEqual(LabelGroup.objects.count(), 1)
        # init
        url = reverse('api:label-detail', args=[2])
        # action
        response = self.client.delete(url, format='json')
        # check
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Label.objects.count(), 0)
        self.assertEqual(LabelGroup.objects.count(), 0)

    def test_list_label(self):
        # init
        label_count = 10
        db_labels = [Label(name='Label %s' % i, group=LabelGroup.objects.create(name='Group %s' % i))
                     for i in range(label_count)]
        db_labels.append(Label(name='Label with empty group'))
        Label.objects.bulk_create(db_labels)
        url = reverse('api:label-list')
        # action
        response = self.client.get(url, format='json')
        # check
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), label_count + 1)
        last_label = response.data.pop()
        for i, label in enumerate(response.data):
            self.assertEqual(label['name'], 'Label %s' % i)
            self.assertEqual(label['group'], 'Group %s' % i)
        self.assertEqual(last_label['name'], 'Label with empty group')
        self.assertEqual(last_label['group'], None)

    def check_label(self):
        self.assertEqual(Label.objects.count(), 1)
        self.assertEqual(LabelGroup.objects.count(), 1)
        db_label = Label.objects.first()
        self.assertEqual(db_label.name, self.label_name)
        self.assertEqual(db_label.group.name, self.group_name)


class LabelTableTests(APITestCase):
    username = 'tester'
    password = 'tester_password'

    def setUp(self):
        test_user = User.objects.create_user(username=self.username, password=self.password)
        self.client.force_authenticate(user=test_user)

    def test_list_group(self):
        # init
        group1 = LabelGroup.objects.create(name='Group1')
        Label.objects.create(name='label11', group=group1)
        Label.objects.create(name='label12', group=group1)
        group1 = LabelGroup.objects.create(name='Group2')
        Label.objects.create(name='label21', group=group1)
        Label.objects.create(name='label22', group=group1)
        Label.objects.create(name='label00', group=None)
        url = reverse('api:label_table')
        # action
        response = self.client.get(url, format='json')
        # check
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        result = response.data
        self.assertEqual(len(result), 3)  # group count
        self.assertTrue('label00' in result['NO_GROUP'])
        self.assertTrue('label11' in result['Group1'])
        self.assertTrue('label12' in result['Group1'])
        self.assertTrue('label21' in result['Group2'])
        self.assertTrue('label22' in result['Group2'])


class LabelGroupTests(APITestCase):
    username = 'tester'
    password = 'tester_password'

    def setUp(self):
        test_user = User.objects.create_user(username=self.username, password=self.password)
        self.client.force_authenticate(user=test_user)

    def test_update_group(self):
        # init
        LabelGroup.objects.create(name='Group1')
        new_group = {'name': 'Group2', 'color': '#aaaaaa'}
        url = reverse('api:labelgroup-detail', args=[1])
        # action
        response = self.client.put(url, new_group, format='json')
        # check
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        group = LabelGroup.objects.first()
        self.assertEqual(group.name, 'Group2')
        self.assertEqual(group.color, '#aaaaaa')


class GoalTests(APITestCase):
    username = 'tester'
    password = 'tester_password'

    def setUp(self):
        test_user = User.objects.create_user(username=self.username, password=self.password)
        self.client.force_authenticate(user=test_user)

    def test_create_worklog_with_labels(self):
        # init
        Label.objects.create(name='label1', group=LabelGroup.objects.create(name='group1'))
        Label.objects.create(name='label2', group=LabelGroup.objects.create(name='group2'))
        worklog_data = {'log': 'worklog1', 'labels': ['label1', 'label2']}
        url = reverse('api:worklog-list')
        # action
        response = self.client.post(url, worklog_data, format='json')
        # check
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        worklog = WorkLog.objects.first()
        self.assertEqual(worklog.log, 'worklog1')
        self.assertEqual(worklog.duration, 30)
        self.assertEqual(worklog.date, date.today())
        labels = list(worklog.labels.all())
        self.assertEqual(len(list(labels)), 2)
        label1, label2 = labels
        self.assertEqual(label1.name, 'label1')
        self.assertEqual(label1.group.name, 'group1')
        self.assertEqual(label2.name, 'label2')
        self.assertEqual(label2.group.name, 'group2')

    def test_create_worklog_without_labels(self):
        # init
        worklog_data = {'log': 'worklog', 'date': '2019-08-13', 'duration': 99}
        url = reverse('api:worklog-list')
        # action
        response = self.client.post(url, worklog_data, format='json')
        # check
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        worklog = WorkLog.objects.first()
        self.assertEqual(worklog.log, 'worklog')
        self.assertEqual(worklog.duration, 99)
        self.assertEqual(worklog.date, date(2019, 8, 13))
        labels = list(worklog.labels.all())
        self.assertEqual(len(list(labels)), 0)

    def test_delete_worklog(self):
        # init
        WorkLog.objects.create(log='worklog')
        url = reverse('api:worklog-detail', args=[1])
        # action
        response = self.client.delete(url, format='json')
        # check
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(WorkLog.objects.count(), 0)

    def test_update_worklog(self):
        # init
        label1 = Label.objects.create(name='label1')
        worklog1 = WorkLog.objects.create(log='worklog1', duration=111)
        worklog1.labels.add(label1)
        worklog1.save()
        Label.objects.create(name='label2')
        new_worklog = {'log': 'worklog2', 'labels': ['label2', 'label1'], 'date': '2019-08-13', 'duration': '112'}
        url = reverse('api:worklog-detail', args=[1])
        # action
        response = self.client.put(url, new_worklog, format='json')
        # check
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        worklog = WorkLog.objects.first()
        self.assertEqual(worklog.log, 'worklog2')
        self.assertEqual(worklog.duration, 112)
        self.assertEqual(worklog.date, date(2019, 8, 13))
        labels = list(worklog.labels.all())
        self.assertEqual(len(list(labels)), 2)

    def test_list_worklog(self):
        # init
        label1 = Label.objects.create(name='label1')
        worklog1 = WorkLog.objects.create(log='worklog1')
        worklog1.labels.add(label1)
        worklog1.save()
        WorkLog.objects.create(log='worklog2')
        url = reverse('api:worklog-list')
        # action
        response = self.client.get(url, format='json')
        # check
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)
        results = response.data['results']
        self.assertEqual(results[1]['log'], 'worklog1')
        self.assertEqual(results[0]['log'], 'worklog2')
        self.assertEqual(results[1]['labels'], ['label1'])
        self.assertEqual(results[0]['labels'], [])
