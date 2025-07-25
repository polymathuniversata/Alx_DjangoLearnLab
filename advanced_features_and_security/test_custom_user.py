#!/usr/bin/env python3
"""
Test script to verify the custom user model implementation.
"""

import os
import sys
import django
from datetime import date

# Add the project directory to the Python path
project_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'LibraryProject')
sys.path.append(project_dir)

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')
django.setup()

from django.contrib.auth import get_user_model
from accounts.models import CustomUser

def test_custom_user_model():
    """Test the custom user model functionality."""
    
    print("Testing Custom User Model Implementation...")
    print("=" * 50)
    
    # Get the custom user model
    User = get_user_model()
    
    # Test 1: Verify the custom user model is being used
    print(f"1. Custom User Model: {User.__name__}")
    print(f"   Model path: {User._meta.app_label}.{User.__name__}")
    assert User.__name__ == 'CustomUser', "Custom user model not being used!"
    print("   ✓ Custom user model is correctly configured")
    
    # Test 2: Check custom fields exist
    print("\n2. Custom Fields:")
    field_names = [field.name for field in User._meta.fields]
    
    assert 'date_of_birth' in field_names, "date_of_birth field missing!"
    print("   ✓ date_of_birth field exists")
    
    assert 'profile_photo' in field_names, "profile_photo field missing!"
    print("   ✓ profile_photo field exists")
    
    # Test 3: Test user creation
    print("\n3. User Creation Test:")
    
    # Clean up any existing test user
    User.objects.filter(username='testuser').delete()
    
    # Create a test user
    test_user = User.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='testpass123',
        date_of_birth=date(1990, 1, 1)
    )
    
    print(f"   ✓ User created: {test_user.username}")
    print(f"   ✓ Email: {test_user.email}")
    print(f"   ✓ Date of birth: {test_user.date_of_birth}")
    
    # Test 4: Test superuser creation
    print("\n4. Superuser Creation Test:")
    
    # Clean up any existing test superuser
    User.objects.filter(username='testsuperuser').delete()
    
    # Create a test superuser
    test_superuser = User.objects.create_superuser(
        username='testsuperuser',
        email='super@example.com',
        password='superpass123',
        date_of_birth=date(1985, 5, 15)
    )
    
    print(f"   ✓ Superuser created: {test_superuser.username}")
    print(f"   ✓ Is staff: {test_superuser.is_staff}")
    print(f"   ✓ Is superuser: {test_superuser.is_superuser}")
    print(f"   ✓ Date of birth: {test_superuser.date_of_birth}")
    
    # Test 5: Test model string representation
    print("\n5. Model String Representation:")
    print(f"   ✓ User str: {str(test_user)}")
    print(f"   ✓ Superuser str: {str(test_superuser)}")
    
    # Clean up test users
    test_user.delete()
    test_superuser.delete()
    
    print("\n" + "=" * 50)
    print("✅ All tests passed! Custom user model is working correctly.")
    print("=" * 50)

if __name__ == '__main__':
    test_custom_user_model()
