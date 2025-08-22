from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import Post, Comment

User = get_user_model()


class PostsAPITestCase(APITestCase):
    def setUp(self):
        """Set up test data"""
        self.user1 = User.objects.create_user(
            username='testuser1',
            email='test1@example.com',
            password='testpass123'
        )
        self.user2 = User.objects.create_user(
            username='testuser2',
            email='test2@example.com',
            password='testpass123'
        )
        
        self.post1 = Post.objects.create(
            title='Test Post 1',
            content='This is test post content 1',
            author=self.user1
        )

    def test_post_list_authenticated(self):
        """Test POST list endpoint for authenticated users"""
        self.client.force_authenticate(user=self.user1)
        response = self.client.get('/api/posts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_create(self):
        """Test creating a new post"""
        self.client.force_authenticate(user=self.user1)
        data = {
            'title': 'New Test Post',
            'content': 'This is new test content'
        }
        response = self.client.post('/api/posts/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'New Test Post')

    def test_post_permissions(self):
        """Test post update permissions"""
        self.client.force_authenticate(user=self.user2)
        data = {'title': 'Unauthorized Update'}
        response = self.client.patch(f'/api/posts/{self.post1.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
