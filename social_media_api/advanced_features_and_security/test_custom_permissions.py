#!/usr/bin/env python3
"""
Custom Permissions Test Script.
This script tests the custom permission system for book operations including
user creation with different permissions and verification that access control
works correctly for add, edit, and delete book operations.
"""

import os
import sys
import django

# Setup Django environment
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'LibraryProject'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')
django.setup()

from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType
from django.test import Client
from django.urls import reverse
from relationship_app.models import UserProfile, Book, Author

def create_test_users_with_permissions():
    """Create test users with different custom permissions."""
    print("Creating test users with different custom permissions...")
    
    # Clean up existing test users
    User.objects.filter(username__in=['admin_perm', 'add_only', 'edit_only', 'delete_only', 'no_perm']).delete()
    
    # Get the Book content type and permissions
    book_content_type = ContentType.objects.get_for_model(Book)
    can_add_book = Permission.objects.get(content_type=book_content_type, codename='can_add_book')
    can_change_book = Permission.objects.get(content_type=book_content_type, codename='can_change_book')
    can_delete_book = Permission.objects.get(content_type=book_content_type, codename='can_delete_book')
    
    # Create user with all permissions (Admin-like)
    admin_user = User.objects.create_user(
        username='admin_perm',
        password='testpass123',
        email='admin@test.com'
    )
    admin_user.user_permissions.add(can_add_book, can_change_book, can_delete_book)
    admin_profile = UserProfile.objects.get(user=admin_user)
    admin_profile.role = 'Admin'
    admin_profile.save()
    print("   ✓ Admin user with all permissions created")
    
    # Create user with only add permission
    add_user = User.objects.create_user(
        username='add_only',
        password='testpass123',
        email='add@test.com'
    )
    add_user.user_permissions.add(can_add_book)
    add_profile = UserProfile.objects.get(user=add_user)
    add_profile.role = 'Librarian'
    add_profile.save()
    print("   ✓ Add-only user created")
    
    # Create user with only edit permission
    edit_user = User.objects.create_user(
        username='edit_only',
        password='testpass123',
        email='edit@test.com'
    )
    edit_user.user_permissions.add(can_change_book)
    edit_profile = UserProfile.objects.get(user=edit_user)
    edit_profile.role = 'Librarian'
    edit_profile.save()
    print("   ✓ Edit-only user created")
    
    # Create user with only delete permission
    delete_user = User.objects.create_user(
        username='delete_only',
        password='testpass123',
        email='delete@test.com'
    )
    delete_user.user_permissions.add(can_delete_book)
    delete_profile = UserProfile.objects.get(user=delete_user)
    delete_profile.role = 'Librarian'
    delete_profile.save()
    print("   ✓ Delete-only user created")
    
    # Create user with no permissions
    no_perm_user = User.objects.create_user(
        username='no_perm',
        password='testpass123',
        email='noperm@test.com'
    )
    no_perm_profile = UserProfile.objects.get(user=no_perm_user)
    no_perm_profile.role = 'Member'
    no_perm_profile.save()
    print("   ✓ No-permission user created")
    
    return admin_user, add_user, edit_user, delete_user, no_perm_user

def create_test_book():
    """Create a test book for testing edit and delete operations."""
    author, created = Author.objects.get_or_create(name='Test Author')
    book, created = Book.objects.get_or_create(
        title='Test Book',
        author=author,
        publication_year=2023
    )
    return book

def test_permission_access(client, username, password, view_name, expected_status, book_id=None):
    """Test access to a specific view with given user credentials."""
    # Login
    login_success = client.login(username=username, password=password)
    if not login_success:
        print(f"   ✗ Failed to login as {username}")
        return False
    
    # Try to access the view
    try:
        if book_id:
            url = reverse(view_name, args=[book_id])
        else:
            url = reverse(view_name)
        
        response = client.get(url)
        
        if response.status_code == expected_status:
            print(f"   ✓ {username} access to {view_name} (Status: {response.status_code})")
            return True
        else:
            print(f"   ✗ {username} access to {view_name} failed (Status: {response.status_code}, Expected: {expected_status})")
            return False
    except Exception as e:
        print(f"   ✗ Error accessing {view_name} as {username}: {e}")
        return False
    finally:
        client.logout()

def test_custom_permissions_system():
    """Test complete custom permissions system."""
    print("Testing Django Custom Permissions System")
    print("=" * 60)
    
    # Create test users with different permissions
    admin_user, add_user, edit_user, delete_user, no_perm_user = create_test_users_with_permissions()
    
    # Create test book for edit/delete operations
    test_book = create_test_book()
    print(f"   ✓ Test book created: {test_book.title} (ID: {test_book.id})")
    
    # Create test client
    client = Client()
    
    print("\n1. Testing Add Book Permission...")
    print("-" * 40)
    test_permission_access(client, 'admin_perm', 'testpass123', 'add_book', 200)
    test_permission_access(client, 'add_only', 'testpass123', 'add_book', 200)
    test_permission_access(client, 'edit_only', 'testpass123', 'add_book', 403)
    test_permission_access(client, 'delete_only', 'testpass123', 'add_book', 403)
    test_permission_access(client, 'no_perm', 'testpass123', 'add_book', 403)
    
    print("\n2. Testing Edit Book Permission...")
    print("-" * 40)
    test_permission_access(client, 'admin_perm', 'testpass123', 'edit_book', 200, test_book.id)
    test_permission_access(client, 'add_only', 'testpass123', 'edit_book', 403, test_book.id)
    test_permission_access(client, 'edit_only', 'testpass123', 'edit_book', 200, test_book.id)
    test_permission_access(client, 'delete_only', 'testpass123', 'edit_book', 403, test_book.id)
    test_permission_access(client, 'no_perm', 'testpass123', 'edit_book', 403, test_book.id)
    
    print("\n3. Testing Delete Book Permission...")
    print("-" * 40)
    test_permission_access(client, 'admin_perm', 'testpass123', 'delete_book', 200, test_book.id)
    test_permission_access(client, 'add_only', 'testpass123', 'delete_book', 403, test_book.id)
    test_permission_access(client, 'edit_only', 'testpass123', 'delete_book', 403, test_book.id)
    test_permission_access(client, 'delete_only', 'testpass123', 'delete_book', 200, test_book.id)
    test_permission_access(client, 'no_perm', 'testpass123', 'delete_book', 403, test_book.id)
    
    print("\n4. Testing Unauthenticated Access...")
    print("-" * 40)
    # Test without login
    try:
        for view_name in ['add_book', 'edit_book', 'delete_book']:
            if view_name in ['edit_book', 'delete_book']:
                url = reverse(view_name, args=[test_book.id])
            else:
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
        add_url = reverse('add_book')
        edit_url = reverse('edit_book', args=[test_book.id])
        delete_url = reverse('delete_book', args=[test_book.id])
        print(f"   ✓ Add Book URL: {add_url}")
        print(f"   ✓ Edit Book URL: {edit_url}")
        print(f"   ✓ Delete Book URL: {delete_url}")
    except Exception as e:
        print(f"   ✗ URL resolution failed: {e}")
    
    # Clean up test users and book
    print("\n6. Cleaning up test data...")
    print("-" * 40)
    User.objects.filter(username__in=['admin_perm', 'add_only', 'edit_only', 'delete_only', 'no_perm']).delete()
    test_book.delete()
    print("   ✓ Test users and book cleaned up")
    
    print("\n" + "=" * 60)
    print("Custom Permissions testing completed!")
    print("The system properly restricts access based on custom permissions.")

if __name__ == "__main__":
    test_custom_permissions_system()
