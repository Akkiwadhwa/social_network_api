from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import Post

User = get_user_model()

class SocialNetworkAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_user_signup(self):
        url = reverse('user_signup')
        data = {
            'email': 'test@example.com',
            'password': 'testpassword',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().email, 'test@example.com')

    def test_user_login(self):
        user = User.objects.create_user(email='test@example.com', password='testpassword')
        url = reverse('token_obtain_pair')
        data = {
            'email': 'test@example.com',
            'password': 'testpassword',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('refresh', response.data)
        self.assertIn('access', response.data)

    def test_get_user_data(self):
        user = User.objects.create_user(email='test@example.com', password='testpassword')
        url = reverse('get_user_data')
        self.client.force_authenticate(user=user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], 'test@example.com')

    def test_post_crud(self):
        user = User.objects.create_user(email='test@example.com', password='testpassword')
        url = reverse('post_list_create')
        self.client.force_authenticate(user=user)
        data = {
            'title': 'Test Post',
            'content': 'This is a test post.',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 1)
        post_id = response.data['id']
        url = reverse('post_retrieve_update_destroy', args=[post_id])
        data = {
            'title': 'Updated Post',
            'content': 'This is an updated post.',
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Updated Post')
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Post.objects.count(), 0)

    def test_post_like_unlike(self):
        user = User.objects.create_user(email='test@example.com', password='testpassword')
        post = Post.objects.create(title='Test Post', content='This is a test post.', user=user)
        url = reverse('post_like', args=[post.id])
        self.client.force_authenticate(user=user)
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(post.likes.count(), 1)
        url = reverse('post_unlike', args=[post.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(post.likes.count(), 0)

