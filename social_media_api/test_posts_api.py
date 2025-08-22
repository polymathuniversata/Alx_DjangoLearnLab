#!/usr/bin/env python
"""
Test script for Posts and Comments API endpoints.
This script tests all CRUD operations, permissions, pagination, and filtering.
"""

import os
import sys
import django
from django.conf import settings

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from posts.models import Post, Comment
from django.urls import reverse
import json

User = get_user_model()


class PostsAPITestCase(APITestCase):
    def setUp(self):
        """Set up test data"""
        # Create test users
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
        
        # Create test posts
        self.post1 = Post.objects.create(
            title='Test Post 1',
            content='This is test post content 1',
            author=self.user1
        )
        self.post2 = Post.objects.create(
            title='Test Post 2',
            content='This is test post content 2',
            author=self.user2
        )
        
        # Create test comments
        self.comment1 = Comment.objects.create(
            post=self.post1,
            author=self.user1,
            content='Test comment 1'
        )
        
        self.client = APIClient()

    def authenticate_user1(self):
        """Authenticate as user1"""
        self.client.force_authenticate(user=self.user1)

    def authenticate_user2(self):
        """Authenticate as user2"""
        self.client.force_authenticate(user=self.user2)

    def test_post_list_authenticated(self):
        """Test POST list endpoint for authenticated users"""
        self.authenticate_user1()
        response = self.client.get('/api/posts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
        self.assertEqual(len(response.data['results']), 2)

    def test_post_list_unauthenticated(self):
        """Test POST list endpoint for unauthenticated users"""
        response = self.client.get('/api/posts/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_create(self):
        """Test creating a new post"""
        self.authenticate_user1()
        data = {
            'title': 'New Test Post',
            'content': 'This is new test content'
        }
        response = self.client.post('/api/posts/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'New Test Post')
        self.assertEqual(response.data['author']['id'], self.user1.id)

    def test_post_detail(self):
        """Test retrieving a specific post"""
        self.authenticate_user1()
        response = self.client.get(f'/api/posts/{self.post1.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Post 1')

    def test_post_update_by_author(self):
        """Test updating post by its author"""
        self.authenticate_user1()
        data = {'title': 'Updated Title', 'content': 'Updated content'}
        response = self.client.patch(f'/api/posts/{self.post1.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Updated Title')

    def test_post_update_by_non_author(self):
        """Test updating post by non-author (should fail)"""
        self.authenticate_user2()
        data = {'title': 'Unauthorized Update'}
        response = self.client.patch(f'/api/posts/{self.post1.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_delete_by_author(self):
        """Test deleting post by its author"""
        self.authenticate_user1()
        response = self.client.delete(f'/api/posts/{self.post1.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_post_delete_by_non_author(self):
        """Test deleting post by non-author (should fail)"""
        self.authenticate_user2()
        response = self.client.delete(f'/api/posts/{self.post1.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_search_by_title(self):
        """Test searching posts by title"""
        self.authenticate_user1()
        response = self.client.get('/api/posts/?search=Test Post 1')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data['results']
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['title'], 'Test Post 1')

    def test_post_filter_by_author(self):
        """Test filtering posts by author"""
        self.authenticate_user1()
        response = self.client.get(f'/api/posts/?author={self.user1.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data['results']
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['author']['id'], self.user1.id)

    def test_comment_create(self):
        """Test creating a new comment"""
        self.authenticate_user1()
        data = {
            'post': self.post1.id,
            'content': 'This is a new comment'
        }
        response = self.client.post('/api/comments/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['content'], 'This is a new comment')
        self.assertEqual(response.data['author']['id'], self.user1.id)

    def test_comment_list_for_post(self):
        """Test listing comments for a specific post"""
        self.authenticate_user1()
        response = self.client.get(f'/api/comments/?post={self.post1.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data['results']
        self.assertEqual(len(results), 1)

    def test_comment_update_by_author(self):
        """Test updating comment by its author"""
        self.authenticate_user1()
        data = {'content': 'Updated comment content'}
        response = self.client.patch(f'/api/comments/{self.comment1.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['content'], 'Updated comment content')

    def test_comment_delete_by_author(self):
        """Test deleting comment by its author"""
        self.authenticate_user1()
        response = self.client.delete(f'/api/comments/{self.comment1.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_my_posts_endpoint(self):
        """Test custom my_posts endpoint"""
        self.authenticate_user1()
        response = self.client.get('/api/posts/my_posts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data['results']
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['author']['id'], self.user1.id)

    def test_my_comments_endpoint(self):
        """Test custom my_comments endpoint"""
        self.authenticate_user1()
        response = self.client.get('/api/comments/my_comments/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data['results']
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['author']['id'], self.user1.id)

    def test_post_comments_endpoint(self):
        """Test getting comments for a specific post"""
        self.authenticate_user1()
        response = self.client.get(f'/api/posts/{self.post1.id}/comments/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['content'], 'Test comment 1')


if __name__ == '__main__':
    import unittest
    
    # Create test suite
    suite = unittest.TestLoader().loadTestsFromTestCase(PostsAPITestCase)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    if result.wasSuccessful():
        print("\\n✅ All tests passed!")
    else:
        print(f"\\n❌ {len(result.failures)} test(s) failed, {len(result.errors)} error(s)")
        
    sys.exit(0 if result.wasSuccessful() else 1)