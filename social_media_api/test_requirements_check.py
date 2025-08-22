#!/usr/bin/env python3
"""
Test script to validate that the implementation meets the specific requirements
for the follow/unfollow and feed functionality.
"""

import os
import sys
import inspect
import re

# Add the project root to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

def check_accounts_views():
    """Check accounts/views.py for required elements."""
    print("Checking accounts/views.py...")
    
    # Read the file
    views_path = os.path.join(project_root, 'accounts', 'views.py')
    with open(views_path, 'r') as f:
        content = f.read()
    
    # Check for required elements
    checks = {
        'generics.GenericAPIView': 'generics.GenericAPIView' in content,
        'CustomUser.objects.all()': 'CustomUser.objects.all()' in content,
    }
    
    for check, passed in checks.items():
        if passed:
            print(f"  ✓ Found: {check}")
        else:
            print(f"  ✗ Missing: {check}")
    
    return all(checks.values())

def check_accounts_urls():
    """Check accounts/urls.py for follow/unfollow routes."""
    print("Checking accounts/urls.py...")
    
    urls_path = os.path.join(project_root, 'accounts', 'urls.py')
    with open(urls_path, 'r') as f:
        content = f.read()
    
    # Check for required routes
    checks = {
        '/follow/<int:user_id>/': 'follow/<int:user_id>/' in content,
        '/unfollow/<int:user_id>/': 'unfollow/<int:user_id>/' in content,
    }
    
    for check, passed in checks.items():
        if passed:
            print(f"  ✓ Found route: {check}")
        else:
            print(f"  ✗ Missing route: {check}")
    
    return all(checks.values())

def check_posts_urls():
    """Check posts/urls.py for feed route."""
    print("Checking posts/urls.py...")
    
    urls_path = os.path.join(project_root, 'posts', 'urls.py')
    with open(urls_path, 'r') as f:
        content = f.read()
    
    # Check for required route
    checks = {
        '/feed/': 'feed/' in content,
    }
    
    for check, passed in checks.items():
        if passed:
            print(f"  ✓ Found route: {check}")
        else:
            print(f"  ✗ Missing route: {check}")
    
    return all(checks.values())

def check_posts_views():
    """Check posts/views.py for feed functionality."""
    print("Checking posts/views.py...")
    
    views_path = os.path.join(project_root, 'posts', 'views.py')
    with open(views_path, 'r') as f:
        content = f.read()
    
    # Check for feed view implementation
    checks = {
        'FeedView': 'class FeedView' in content,
        'following users': 'following' in content and 'users' in content,
        'ordered by creation date': '-created_at' in content or 'creation date' in content,
    }
    
    for check, passed in checks.items():
        if passed:
            print(f"  ✓ Found: {check}")
        else:
            print(f"  ✗ Missing: {check}")
    
    return all(checks.values())

def main():
    """Run all checks."""
    print("="*60)
    print("CHECKING FOLLOW/UNFOLLOW AND FEED REQUIREMENTS")
    print("="*60)
    
    results = []
    
    # Check all components
    results.append(check_accounts_views())
    print()
    results.append(check_accounts_urls()) 
    print()
    results.append(check_posts_urls())
    print()
    results.append(check_posts_views())
    print()
    
    # Summary
    print("="*60)
    if all(results):
        print("✅ ALL REQUIREMENTS CHECKS PASSED!")
    else:
        print("❌ SOME REQUIREMENTS CHECKS FAILED!")
        print("   Please review the missing items above.")
    print("="*60)
    
    return all(results)

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
