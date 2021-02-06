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
        db_post = Post.objects.get()
        self.check_post(db_post)
        self.assertEqual(db_post.deleted, False)

    def test_delete_post(self):
        # init
        url = reverse('api:post-detail', args=[1])
        user = User.objects.get(username=self.username)
        Post.objects.create(user=user, **self.test_post).save()
        # action
        response = self.client.delete(url, format='json')
        # check
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Post.objects.count(), 0)
        self.assertEqual(Post.all_objects.count(), 1)
        deleted_post = Post.all_objects.get()
        self.check_post(deleted_post)
        self.assertEqual(deleted_post.deleted, True)

    def check_post(self, post):
        self.assertEqual(post.title, self.title)
        self.assertEqual(post.body, self.body)
        self.assertEqual(post.user.username, self.username)
