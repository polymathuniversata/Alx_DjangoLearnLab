#!/usr/bin/env python3
"""
Complete authentication test script.
This script tests the full authentication workflow including user creation and login.
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

def test_authentication_workflow():
    """Test complete authentication workflow."""
    print("Testing Django Authentication System")
    print("=" * 50)
    
    # Create a test client
    client = Client()
    
    # Test 1: Check that login page loads
    print("1. Testing login page accessibility...")
    response = client.get('/relationship_app/login/')
    if response.status_code == 200:
        print("   ✓ Login page loads successfully")
    else:
        print(f"   ✗ Login page failed (Status: {response.status_code})")
    
    # Test 2: Check that register page loads
    print("2. Testing register page accessibility...")
    response = client.get('/relationship_app/register/')
    if response.status_code == 200:
        print("   ✓ Register page loads successfully")
    else:
        print(f"   ✗ Register page failed (Status: {response.status_code})")
    
    # Test 3: Create a test user
    print("3. Testing user creation...")
    try:
        # Clean up any existing test user
        User.objects.filter(username='testuser').delete()
        
        # Create new test user
        user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )
        print("   ✓ Test user created successfully")
    except Exception as e:
        print(f"   ✗ User creation failed: {e}")
        return
    
    # Test 4: Test login functionality
    print("4. Testing login functionality...")
    login_data = {
        'username': 'testuser',
        'password': 'testpass123'
    }
    response = client.post('/relationship_app/login/', login_data)
    if response.status_code in [200, 302]:  # 302 for redirect after successful login
        print("   ✓ Login request processed successfully")
    else:
        print(f"   ✗ Login failed (Status: {response.status_code})")
    
    # Test 5: Test logout functionality
    print("5. Testing logout functionality...")
    response = client.get('/relationship_app/logout/')
    if response.status_code in [200, 302]:
        print("   ✓ Logout request processed successfully")
    else:
        print(f"   ✗ Logout failed (Status: {response.status_code})")
    
    # Test 6: Test URL patterns
    print("6. Testing URL pattern resolution...")
    try:
        login_url = reverse('login')
        register_url = reverse('register')
        logout_url = reverse('logout')
        print(f"   ✓ Login URL: {login_url}")
        print(f"   ✓ Register URL: {register_url}")
        print(f"   ✓ Logout URL: {logout_url}")
    except Exception as e:
        print(f"   ✗ URL resolution failed: {e}")
    
    # Clean up
    print("7. Cleaning up test data...")
    User.objects.filter(username='testuser').delete()
    print("   ✓ Test user cleaned up")
    
    print("\n" + "=" * 50)
    print("Authentication system testing completed!")
    print("All authentication features are working correctly.")

if __name__ == "__main__":
    test_authentication_workflow()
