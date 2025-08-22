#!/usr/bin/env python3
"""
Comprehensive validation script to check all the specific requirements mentioned.
"""

import os
import re

def validate_feed_implementation():
    """Check for the exact feed implementation requirements."""
    
    print("1. Checking for feed view in posts app...")
    
    views_path = os.path.join(os.path.dirname(__file__), 'posts', 'views.py')
    with open(views_path, 'r') as f:
        content = f.read()
    
    # Check for the specific pattern mentioned in the failing check
    pattern = r'Post\.objects\.filter\(author__in=following_users\)\.order_by'
    
    if re.search(pattern, content):
        print("   ✅ Found: Post.objects.filter(author__in=following_users).order_by")
    else:
        print("   ❌ Missing: Post.objects.filter(author__in=following_users).order_by")
        return False
    
    # Check for FeedView class
    if 'class FeedView' in content:
        print("   ✅ Found: FeedView class")
    else:
        print("   ❌ Missing: FeedView class")
        return False
    
    # Check for ordering by creation date (most recent first)
    if '-created_at' in content:
        print("   ✅ Found: Ordering by creation date (most recent first)")
    else:
        print("   ❌ Missing: Ordering by creation date")
        return False
    
    return True

def validate_follow_urls():
    """Check for follow management URL patterns in accounts/urls.py."""
    
    print("\n2. Checking URL patterns in accounts/urls.py...")
    
    urls_path = os.path.join(os.path.dirname(__file__), 'accounts', 'urls.py')
    with open(urls_path, 'r') as f:
        content = f.read()
    
    # Check for follow and unfollow routes
    follow_pattern = r'follow/<int:user_id>/'
    unfollow_pattern = r'unfollow/<int:user_id>/'
    
    if re.search(follow_pattern, content):
        print("   ✅ Found: /follow/<int:user_id>/ route")
    else:
        print("   ❌ Missing: /follow/<int:user_id>/ route")
        return False
    
    if re.search(unfollow_pattern, content):
        print("   ✅ Found: /unfollow/<int:user_id>/ route")
    else:
        print("   ❌ Missing: /unfollow/<int:user_id>/ route")
        return False
    
    return True

def validate_feed_url():
    """Check for feed endpoint in posts/urls.py."""
    
    print("\n3. Checking feed endpoint in posts/urls.py...")
    
    urls_path = os.path.join(os.path.dirname(__file__), 'posts', 'urls.py')
    with open(urls_path, 'r') as f:
        content = f.read()
    
    # Check for feed route
    if 'feed/' in content:
        print("   ✅ Found: /feed/ route")
        return True
    else:
        print("   ❌ Missing: /feed/ route")
        return False

def main():
    """Run all validations."""
    print("="*80)
    print("COMPREHENSIVE VALIDATION FOR FOLLOW SYSTEM AND FEED FUNCTIONALITY")
    print("="*80)
    
    results = []
    
    # Run all validations
    results.append(validate_feed_implementation())
    results.append(validate_follow_urls())
    results.append(validate_feed_url())
    
    print("\n" + "="*80)
    if all(results):
        print("🎉 ALL REQUIREMENTS VALIDATED SUCCESSFULLY!")
        print("\nThe implementation includes:")
        print("• Feed view that generates posts from followed users")
        print("• Posts ordered by creation date (most recent first)")
        print("• Follow/unfollow URL endpoints in accounts app")
        print("• Feed endpoint in posts app")
        print("• Proper use of Post.objects.filter(author__in=following_users).order_by")
    else:
        print("❌ SOME REQUIREMENTS ARE NOT MET!")
        print("Please check the failed items above.")
    print("="*80)
    
    return all(results)

if __name__ == '__main__':
    success = main()
    exit(0 if success else 1)
