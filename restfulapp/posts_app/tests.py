from django.conf import settings

settings.configure(DEBUG=True)

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status

from .models import Post, Like

class ModelsTestCase(TestCase):
    """Test Post and Like models"""
    def setUp(self):
        """Prepare data for testing. Create user, post and like"""
        self.user = User(
            username='foobar',
            email='foobar123@gmail.com',
            password='foobar777'
        )
        self.post = Post(
            title='Sample',
            content='Lorem ipsum',
            author=self.user
        )
        self.like = Like(user=self.user, post=self.post)

    def create_post_test(self):
        #count post objects
        num = Post.objects.count()
        self.post.save()
        #and compare with number of posts we are expecting for
        self.assertEqual(Post.objects.count(), num+1)

    def create_like_test(self):
        #do the same with likes
        num = Like.objects.count()
        self.like.save()
        self.assertEqual(Like.objects.count(), num+1)

class PostViewTestCase(TestCase):
    """Test handling with posts"""
    def setUp(self):
        """Prepare data for testing. APIClient allows us to simulate clients actions"""
        self.client = APIClient

        self.user = User(
            username='foobar',
            email='foobar123@gmail.com',
            password='foobar777'
        )
        self.post = Post(
            title='Sample',
            content='Lorem ipsum',
            author=self.user
        )

        self.post_data = {
            'title': 'Sample',
            'content': 'Lorem ipsum'
        }

    def create_post_authenticated_test(self):
        #try to create post properly, with authentication
        self.client.force_authenticate(user=self.user)
        response = self.client.post(reverse('create_post'), self.post_data)
        self.client.logout()
        #it does't make sense to check whether a post has been created
        #we already check creating in ModelsTestCase
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def create_post_non_authenticated_test(self):
        #try to create post without authentication, status 401 expected
        response = self.client.post(reverse('create_post'), self.post_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def get_existing_post_test(self):
        #try to get an existing post
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse('get_post', pk=self.post.id))
        self.client.logout()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def get_nonexisting_post_test(self):
        #try to get a nonexisting post, status 404 expected
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse('get_post', pk=999))
        self.client.logout()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def like_existing_post_test(self):
        #try to like an existing post
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse('like_post', pk=self.post.id))
        self.client.logout()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def like_nonexisting_post(self):
        #try to like a non existing post, status 404 expected
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse('like_post', pk=999))
        self.client.logout()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)