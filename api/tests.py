from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from api.models import Post, Label, LabelGroup


class BlogTests(APITestCase):
    username = 'tester'
    password = 'tester_password'
    title = 'My test title'
    body = 'My test body'

    def setUp(self):
        test_user = User.objects.create_user(username=self.username, password=self.password)
        self.client.force_authenticate(user=test_user)
        self.test_post = {'title': self.title, 'body': self.body}

    def test_create_post(self):
        # init
        url = reverse('api:post-list')
        # action
        response = self.client.post(url, self.test_post, format='json')
        # check
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 1)
        db_post = Post.objects.first()
        self.check_post(db_post)
        self.assertEqual(db_post.deleted, False)

    def test_delete_post(self):
        # init
        url = reverse('api:post-detail', args=[1])
        db_user = User.objects.get(username=self.username)
        Post.objects.create(user=db_user, **self.test_post)
        # action
        response = self.client.delete(url, format='json')
        # check
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Post.objects.count(), 0)
        self.assertEqual(Post.all_objects.count(), 1)
        deleted_post = Post.all_objects.get()
        self.check_post(deleted_post)
        self.assertEqual(deleted_post.deleted, True)

    def test_update_post(self):
        # init
        url = reverse('api:post-detail', args=[1])
        db_user = User.objects.get(username=self.username)
        Post.objects.create(user=db_user, **self.test_post)
        new_test_post = {'title': 'new title', 'body': 'new body'}
        # action
        response = self.client.put(url, new_test_post, format='json')
        # check
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        db_post = Post.objects.first()
        self.check_post(db_post, 'new title', 'new body')
        self.assertEqual(db_post.deleted, False)

    def test_list_post(self):
        # init
        post_count = 10
        url = reverse('api:post-list')
        db_user = User.objects.get(username=self.username)
        db_posts = [Post(title='Title %s' % i, body='Body %s' % i, user=db_user) for i in range(post_count)]
        Post.objects.bulk_create(db_posts)
        # action
        response = self.client.get(url, format='json')
        # check
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], post_count)
        self.assertEqual(response.data['page_count'], 1)
        self.assertEqual(response.data['page_number'], 1)
        self.assertEqual(response.data['page_size'], 100)
        for i, post in enumerate(response.data['results']):
            self.assertEqual(post['title'], 'Title %s' % i)
            self.assertEqual(post['body'], 'Body %s' % i)

    def check_post(self, post, title=title, body=body):
        self.assertEqual(post.title, title)
        self.assertEqual(post.body, body)
        self.assertEqual(post.user.username, self.username)


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
        LabelGroup.objects.create(name=self.group_name, single=True)
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
        group = LabelGroup.objects.create(name=self.group_name, single=True)
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
        group = LabelGroup.objects.create(name=self.group_name, single=True)
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
        db_labels = [Label(name='Label %s' % i, group=LabelGroup.objects.create(name='Group %s' % i, single=True))
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
        group = LabelGroup.objects.create(name='Group1', single=False)
        new_group = {'name': 'Group2', 'single': True}
        url = reverse('api:labelgroup-detail', args=[1])
        # action
        response = self.client.put(url, new_group, format='json')
        # check
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        group = LabelGroup.objects.first()
        self.assertEqual(group.name, 'Group2')
        self.assertEqual(group.single, True)
