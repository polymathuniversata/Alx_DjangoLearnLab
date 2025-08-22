#!/usr/bin/env python3
"""
Comprehensive validation for likes and notifications functionality
"""

import os
import re

def check_required_files():
    """Check if all required files exist."""
    files_to_check = [
        "posts/models.py",
        "posts/views.py", 
        "posts/urls.py",
        "notifications/models.py",
        "notifications/views.py",
        "notifications/urls.py"
    ]
    
    print("Checking required files...")
    all_exist = True
    
    for file_path in files_to_check:
        if os.path.exists(file_path):
            print(f"   ✅ {file_path}")
        else:
            print(f"   ❌ {file_path} - Not found")
            all_exist = False
    
    return all_exist

def check_like_model():
    """Check if Like model exists in posts/models.py."""
    file_path = "posts/models.py"
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print("\nChecking Like model...")
    
    patterns = [
        "class Like(models.Model):",
        "ForeignKey(User",
        "ForeignKey(Post"
    ]
    
    all_found = True
    for pattern in patterns:
        if pattern in content:
            print(f"   ✅ Found: {pattern}")
        else:
            print(f"   ❌ Missing: {pattern}")
            all_found = False
    
    return all_found

def check_notification_model():
    """Check if Notification model exists in notifications/models.py."""
    file_path = "notifications/models.py"
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print("\nChecking Notification model...")
    
    patterns = [
        "class Notification(models.Model):",
        "recipient = models.ForeignKey(User",
        "actor = models.ForeignKey(User", 
        "verb = models.CharField",
        "GenericForeignKey"
    ]
    
    all_found = True
    for pattern in patterns:
        if pattern in content:
            print(f"   ✅ Found: {pattern}")
        else:
            print(f"   ❌ Missing: {pattern}")
            all_found = False
    
    return all_found

def check_like_views():
    """Check if like/unlike views exist with required patterns."""
    file_path = "posts/views.py"
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print("\nChecking like/unlike views...")
    
    required_patterns = [
        "generics.get_object_or_404(Post, pk=pk)",
        "Like.objects.get_or_create(user=request.user, post=post)",
        "class LikePostView",
        "class UnlikePostView"
    ]
    
    all_found = True
    for pattern in required_patterns:
        if pattern in content:
            print(f"   ✅ Found: {pattern}")
        else:
            print(f"   ❌ Missing: {pattern}")
            all_found = False
    
    return all_found

def check_url_patterns():
    """Check if URL patterns are correctly configured."""
    file_path = "posts/urls.py"
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print("\nChecking URL patterns...")
    
    patterns = [
        r"<int:pk>/like/",
        r"<int:pk>/unlike/",
        "LikePostView",
        "UnlikePostView"
    ]
    
    all_found = True
    for pattern in patterns:
        if re.search(pattern, content):
            print(f"   ✅ Found: {pattern}")
        else:
            print(f"   ❌ Missing: {pattern}")
            all_found = False
    
    return all_found

def check_notification_creation():
    """Check if notifications are created in views."""
    file_path = "posts/views.py"
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print("\nChecking notification creation...")
    
    patterns = [
        "from notifications.models import Notification",
        "Notification.objects.create",
        "ContentType.objects.get_for_model"
    ]
    
    all_found = True
    for pattern in patterns:
        if pattern in content:
            print(f"   ✅ Found: {pattern}")
        else:
            print(f"   ❌ Missing: {pattern}")
            all_found = False
    
    return all_found

def main():
    """Main validation function."""
    print("=" * 80)
    print("COMPREHENSIVE LIKES AND NOTIFICATIONS VALIDATION")
    print("=" * 80)
    
    results = []
    
    results.append(check_required_files())
    results.append(check_like_model())
    results.append(check_notification_model())
    results.append(check_like_views())
    results.append(check_url_patterns())
    results.append(check_notification_creation())
    
    print("\n" + "=" * 80)
    
    if all(results):
        print("🎉 ALL VALIDATIONS PASSED!")
        print("✅ All required files exist")
        print("✅ Like model is properly implemented")
        print("✅ Notification model is properly implemented")
        print("✅ Like/unlike views contain required patterns")
        print("✅ URL patterns are correctly configured")
        print("✅ Notification creation is implemented")
    else:
        print("❌ SOME VALIDATIONS FAILED!")
        
        checks = [
            "Required files check",
            "Like model check", 
            "Notification model check",
            "Like views check",
            "URL patterns check",
            "Notification creation check"
        ]
        
        for i, result in enumerate(results):
            status = "✅" if result else "❌"
            print(f"{status} {checks[i]}")
    
    print("=" * 80)

if __name__ == "__main__":
    main()
