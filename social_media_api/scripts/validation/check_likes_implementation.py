#!/usr/bin/env python3
"""
Simple check for likes functionality implementation
"""

import os
import re

def check_posts_views():
    """Check if posts/views.py contains the required patterns."""
    views_file = "posts/views.py"
    
    if not os.path.exists(views_file):
        print(f"❌ {views_file} not found")
        return False
    
    with open(views_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check for required patterns
    required_patterns = [
        "generics.get_object_or_404(Post, pk=pk)",
        "Like.objects.get_or_create(user=request.user, post=post)"
    ]
    
    print(f"Checking {views_file}...")
    all_found = True
    
    for pattern in required_patterns:
        if pattern in content:
            print(f"   ✅ Found: {pattern}")
        else:
            print(f"   ❌ Missing: {pattern}")
            all_found = False
    
    return all_found

def check_posts_urls():
    """Check if posts/urls.py contains the required URL patterns."""
    urls_file = "posts/urls.py"
    
    if not os.path.exists(urls_file):
        print(f"❌ {urls_file} not found")
        return False
    
    with open(urls_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check for like and unlike URL patterns
    patterns_to_find = [
        r"<int:pk>/like/",
        r"<int:pk>/unlike/"
    ]
    
    print(f"\nChecking {urls_file}...")
    all_found = True
    
    for pattern in patterns_to_find:
        if re.search(pattern, content):
            print(f"   ✅ Found URL pattern: {pattern}")
        else:
            print(f"   ❌ Missing URL pattern: {pattern}")
            all_found = False
    
    return all_found

def main():
    """Main validation function."""
    print("================================================================================")
    print("CHECKING LIKES FUNCTIONALITY IMPLEMENTATION")
    print("================================================================================")
    
    views_ok = check_posts_views()
    urls_ok = check_posts_urls()
    
    print("\n" + "="*80)
    
    if views_ok and urls_ok:
        print("🎉 ALL CHECKS PASSED!")
        print("✅ posts/views.py contains required patterns")
        print("✅ posts/urls.py contains required URL patterns")
    else:
        print("❌ SOME CHECKS FAILED!")
        if not views_ok:
            print("❌ posts/views.py missing required patterns")
        if not urls_ok:
            print("❌ posts/urls.py missing required URL patterns")
    
    print("="*80)

if __name__ == "__main__":
    main()
