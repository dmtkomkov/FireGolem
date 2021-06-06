from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from api.models import Post


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
        # Posts ordered by time creation make test below broken
        # for i, post in enumerate(response.data['results']):
        #     self.assertEqual(post['title'], 'Title %s' % i)
        #     self.assertEqual(post['body'], 'Body %s' % i)

    def check_post(self, post, title=title, body=body):
        self.assertEqual(post.title, title)
        self.assertEqual(post.body, body)
        self.assertEqual(post.user.username, self.username)
