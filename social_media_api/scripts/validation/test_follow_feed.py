#!/usr/bin/env python
"""
Test script for Follow and Feed functionality.
This script tests follow/unfollow operations and feed generation.
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


class FollowFeedTestCase(APITestCase):
    def setUp(self):
        """Set up test data"""
        # Create test users
        self.user1 = User.objects.create_user(
            username='user1',
            email='user1@example.com',
            password='testpass123'
        )
        self.user2 = User.objects.create_user(
            username='user2',
            email='user2@example.com',
            password='testpass123'
        )
        self.user3 = User.objects.create_user(
            username='user3',
            email='user3@example.com',
            password='testpass123'
        )
        
        # Create test posts
        self.post1 = Post.objects.create(
            title='User1 Post 1',
            content='This is user1 post content 1',
            author=self.user1
        )
        self.post2 = Post.objects.create(
            title='User2 Post 1',
            content='This is user2 post content 1',
            author=self.user2
        )
        self.post3 = Post.objects.create(
            title='User3 Post 1',
            content='This is user3 post content 1',
            author=self.user3
        )
        
        self.client = APIClient()

    def authenticate_user(self, user):
        """Authenticate as specified user"""
        self.client.force_authenticate(user=user)

    def test_follow_user_success(self):
        """Test successfully following a user"""
        self.authenticate_user(self.user1)
        response = self.client.post(f'/api/auth/follow/{self.user2.id}/')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('followed', response.data['status'])
        
        # Verify the relationship exists
        self.assertTrue(self.user1.following.filter(id=self.user2.id).exists())

    def test_follow_nonexistent_user(self):
        """Test following a user that doesn't exist"""
        self.authenticate_user(self.user1)
        response = self.client.post('/api/auth/follow/99999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_follow_self(self):
        """Test that users cannot follow themselves"""
        self.authenticate_user(self.user1)
        response = self.client.post(f'/api/auth/follow/{self.user1.id}/')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_follow_already_following(self):
        """Test following a user already being followed"""
        # First follow
        self.authenticate_user(self.user1)
        self.client.post(f'/api/auth/follow/{self.user2.id}/')
        
        # Try to follow again
        response = self.client.post(f'/api/auth/follow/{self.user2.id}/')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unfollow_user_success(self):
        """Test successfully unfollowing a user"""
        # First follow
        self.authenticate_user(self.user1)
        self.client.post(f'/api/auth/follow/{self.user2.id}/')
        
        # Then unfollow
        response = self.client.post(f'/api/auth/unfollow/{self.user2.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('unfollowed', response.data['status'])
        
        # Verify the relationship no longer exists
        self.assertFalse(self.user1.following.filter(id=self.user2.id).exists())

    def test_unfollow_not_following(self):
        """Test unfollowing a user not being followed"""
        self.authenticate_user(self.user1)
        response = self.client.post(f'/api/auth/unfollow/{self.user2.id}/')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_feed_empty(self):
        """Test feed when not following anyone"""
        self.authenticate_user(self.user1)
        response = self.client.get('/api/feed/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)
        self.assertEqual(len(response.data['results']), 0)

    def test_feed_with_following(self):
        """Test feed shows posts from followed users"""
        # User1 follows user2 and user3
        self.authenticate_user(self.user1)
        self.client.post(f'/api/auth/follow/{self.user2.id}/')
        self.client.post(f'/api/auth/follow/{self.user3.id}/')
        
        # Check feed
        response = self.client.get('/api/feed/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)  # Should show user2 and user3 posts
        
        # Verify posts are from followed users only
        post_authors = [post['author']['id'] for post in response.data['results']]
        self.assertIn(self.user2.id, post_authors)
        self.assertIn(self.user3.id, post_authors)
        self.assertNotIn(self.user1.id, post_authors)  # Own posts shouldn't appear

    def test_feed_ordering(self):
        """Test that feed posts are ordered by creation date (most recent first)"""
        # Create additional posts with different timestamps
        newer_post = Post.objects.create(
            title='Newer User2 Post',
            content='This is a newer post from user2',
            author=self.user2
        )
        
        # User1 follows user2
        self.authenticate_user(self.user1)
        self.client.post(f'/api/auth/follow/{self.user2.id}/')
        
        # Check feed ordering
        response = self.client.get('/api/feed/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        posts = response.data['results']
        if len(posts) > 1:
            # First post should be the newer one
            self.assertEqual(posts[0]['title'], 'Newer User2 Post')

    def test_feed_unauthenticated(self):
        """Test that unauthenticated users cannot access feed"""
        response = self.client.get('/api/feed/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_follow_endpoints_unauthenticated(self):
        """Test that unauthenticated users cannot follow/unfollow"""
        # Test follow
        response = self.client.post(f'/api/auth/follow/{self.user2.id}/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        # Test unfollow
        response = self.client.post(f'/api/auth/unfollow/{self.user2.id}/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_follower_following_counts(self):
        """Test that user follower and following counts work correctly"""
        # User1 follows user2 and user3
        self.user1.following.add(self.user2, self.user3)
        
        # User2 follows user1
        self.user2.following.add(self.user1)
        
        # Check counts
        self.assertEqual(self.user1.following_count, 2)  # user1 follows 2 users
        self.assertEqual(self.user1.follower_count, 1)   # user1 has 1 follower
        
        self.assertEqual(self.user2.following_count, 1)  # user2 follows 1 user
        self.assertEqual(self.user2.follower_count, 1)   # user2 has 1 follower


if __name__ == '__main__':
    import unittest
    
    # Create test suite
    suite = unittest.TestLoader().loadTestsFromTestCase(FollowFeedTestCase)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    if result.wasSuccessful():
        print("\\n✅ All follow and feed tests passed!")
    else:
        print(f"\\n❌ {len(result.failures)} test(s) failed, {len(result.errors)} error(s)")
        for failure in result.failures:
            print(f"FAIL: {failure[0]}")
            print(failure[1])
        for error in result.errors:
            print(f"ERROR: {error[0]}")
            print(error[1])
        
    sys.exit(0 if result.wasSuccessful() else 1)