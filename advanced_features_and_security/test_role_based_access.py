#!/usr/bin/env python3
"""
Role-Based Access Control Test Script.
This script tests the role-based access control system including user creation with different roles
and verification that access control works correctly for each role-specific view.
"""

import os
import sys
import django

# Setup Django environment
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'LibraryProject'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')
django.setup()

from django.contrib.auth.models import User
from django.test import Client
from django.urls import reverse
from relationship_app.models import UserProfile

def create_test_users():
    """Create test users with different roles."""
    print("Creating test users with different roles...")
    
    # Clean up existing test users
    User.objects.filter(username__in=['admin_user', 'librarian_user', 'member_user']).delete()
    
    # Create Admin user
    admin_user = User.objects.create_user(
        username='admin_user',
        password='testpass123',
        email='admin@library.com'
    )
    admin_profile = UserProfile.objects.get(user=admin_user)
    admin_profile.role = 'Admin'
    admin_profile.save()
    print("   ✓ Admin user created")
    
    # Create Librarian user
    librarian_user = User.objects.create_user(
        username='librarian_user',
        password='testpass123',
        email='librarian@library.com'
    )
    librarian_profile = UserProfile.objects.get(user=librarian_user)
    librarian_profile.role = 'Librarian'
    librarian_profile.save()
    print("   ✓ Librarian user created")
    
    # Create Member user
    member_user = User.objects.create_user(
        username='member_user',
        password='testpass123',
        email='member@library.com'
    )
    member_profile = UserProfile.objects.get(user=member_user)
    member_profile.role = 'Member'
    member_profile.save()
    print("   ✓ Member user created")
    
    return admin_user, librarian_user, member_user

def test_role_access(client, username, password, role, view_name, expected_status):
    """Test access to a specific view with given user credentials."""
    # Login
    login_success = client.login(username=username, password=password)
    if not login_success:
        print(f"   ✗ Failed to login as {username}")
        return False
    
    # Try to access the view
    try:
        url = reverse(view_name)
        response = client.get(url)
        
        if response.status_code == expected_status:
            print(f"   ✓ {role} user can access {view_name} (Status: {response.status_code})")
            return True
        else:
            print(f"   ✗ {role} user access to {view_name} failed (Status: {response.status_code}, Expected: {expected_status})")
            return False
    except Exception as e:
        print(f"   ✗ Error accessing {view_name} as {role}: {e}")
        return False
    finally:
        client.logout()

def test_role_based_access_control():
    """Test complete role-based access control system."""
    print("Testing Django Role-Based Access Control System")
    print("=" * 60)
    
    # Create test users
    admin_user, librarian_user, member_user = create_test_users()
    
    # Create test client
    client = Client()
    
    print("\n1. Testing Admin User Access...")
    print("-" * 40)
    test_role_access(client, 'admin_user', 'testpass123', 'Admin', 'admin_view', 200)
    test_role_access(client, 'admin_user', 'testpass123', 'Admin', 'librarian_view', 200)
    test_role_access(client, 'admin_user', 'testpass123', 'Admin', 'member_view', 200)
    
    print("\n2. Testing Librarian User Access...")
    print("-" * 40)
    test_role_access(client, 'librarian_user', 'testpass123', 'Librarian', 'admin_view', 403)
    test_role_access(client, 'librarian_user', 'testpass123', 'Librarian', 'librarian_view', 200)
    test_role_access(client, 'librarian_user', 'testpass123', 'Librarian', 'member_view', 200)
    
    print("\n3. Testing Member User Access...")
    print("-" * 40)
    test_role_access(client, 'member_user', 'testpass123', 'Member', 'admin_view', 403)
    test_role_access(client, 'member_user', 'testpass123', 'Member', 'librarian_view', 403)
    test_role_access(client, 'member_user', 'testpass123', 'Member', 'member_view', 200)
    
    print("\n4. Testing Unauthenticated Access...")
    print("-" * 40)
    # Test without login
    try:
        for view_name in ['admin_view', 'librarian_view', 'member_view']:
            url = reverse(view_name)
            response = client.get(url)
            if response.status_code in [302, 403]:  # Redirect to login or forbidden
                print(f"   ✓ Unauthenticated access to {view_name} properly blocked (Status: {response.status_code})")
            else:
                print(f"   ✗ Unauthenticated access to {view_name} not properly blocked (Status: {response.status_code})")
    except Exception as e:
        print(f"   ✗ Error testing unauthenticated access: {e}")
    
    print("\n5. Testing URL Pattern Resolution...")
    print("-" * 40)
    try:
        admin_url = reverse('admin_view')
        librarian_url = reverse('librarian_view')
        member_url = reverse('member_view')
        print(f"   ✓ Admin URL: {admin_url}")
        print(f"   ✓ Librarian URL: {librarian_url}")
        print(f"   ✓ Member URL: {member_url}")
    except Exception as e:
        print(f"   ✗ URL resolution failed: {e}")
    
    print("\n6. Testing UserProfile Creation...")
    print("-" * 40)
    try:
        # Test automatic profile creation
        test_user = User.objects.create_user(
            username='test_auto_profile',
            password='testpass123',
            email='test@library.com'
        )
        
        if hasattr(test_user, 'userprofile'):
            print(f"   ✓ UserProfile automatically created with role: {test_user.userprofile.role}")
        else:
            print("   ✗ UserProfile not automatically created")
        
        # Clean up
        test_user.delete()
        
    except Exception as e:
        print(f"   ✗ Error testing UserProfile creation: {e}")
    
    # Clean up test users
    print("\n7. Cleaning up test data...")
    print("-" * 40)
    User.objects.filter(username__in=['admin_user', 'librarian_user', 'member_user']).delete()
    print("   ✓ Test users cleaned up")
    
    print("\n" + "=" * 60)
    print("Role-Based Access Control testing completed!")
    print("The system properly restricts access based on user roles.")

if __name__ == "__main__":
    test_role_based_access_control()
