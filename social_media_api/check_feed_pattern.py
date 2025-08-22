#!/usr/bin/env python3
"""
Simple script to check if the required pattern exists in the code.
"""

import os
import re

def check_feed_pattern():
    """Check if the exact pattern exists in posts/views.py"""
    
    # Read posts/views.py
    views_path = os.path.join(os.path.dirname(__file__), 'posts', 'views.py')
    
    with open(views_path, 'r') as f:
        content = f.read()
    
    # Check for the exact pattern
    pattern = r'Post\.objects\.filter\(author__in=following_users\)\.order_by'
    
    if re.search(pattern, content):
        print("✅ Pattern found: Post.objects.filter(author__in=following_users).order_by")
        return True
    else:
        print("❌ Pattern NOT found: Post.objects.filter(author__in=following_users).order_by")
        return False

def check_urls():
    """Check URL patterns"""
    
    # Check accounts URLs
    accounts_urls_path = os.path.join(os.path.dirname(__file__), 'accounts', 'urls.py')
    with open(accounts_urls_path, 'r') as f:
        accounts_content = f.read()
    
    # Check posts URLs
    posts_urls_path = os.path.join(os.path.dirname(__file__), 'posts', 'urls.py')
    with open(posts_urls_path, 'r') as f:
        posts_content = f.read()
    
    # Check patterns
    follow_pattern = 'follow/<int:user_id>/'
    unfollow_pattern = 'unfollow/<int:user_id>/'
    feed_pattern = 'feed/'
    
    checks = {
        'Follow URL pattern': follow_pattern in accounts_content,
        'Unfollow URL pattern': unfollow_pattern in accounts_content,
        'Feed URL pattern': feed_pattern in posts_content,
    }
    
    for check, passed in checks.items():
        if passed:
            print(f"✅ {check}: Found")
        else:
            print(f"❌ {check}: NOT Found")
    
    return all(checks.values())

if __name__ == '__main__':
    print("Checking required patterns...")
    print("="*50)
    
    feed_ok = check_feed_pattern()
    urls_ok = check_urls()
    
    print("="*50)
    if feed_ok and urls_ok:
        print("✅ ALL PATTERNS FOUND!")
    else:
        print("❌ SOME PATTERNS MISSING!")
