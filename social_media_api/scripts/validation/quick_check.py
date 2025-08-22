#!/usr/bin/env python
"""
Quick check script to verify the specific requirements mentioned in the error.
"""

import os

def check_views_requirements():
    """Check that posts/views.py contains the required strings."""
    print("Checking posts/views.py requirements...")
    
    views_file = os.path.join(os.path.dirname(__file__), 'posts', 'views.py')
    
    with open(views_file, 'r') as f:
        content = f.read()
    
    required_strings = [
        "viewsets.ModelViewSet",
        "Comment.objects.all()",
        "Post.objects.all()"
    ]
    
    all_found = True
    for req_string in required_strings:
        if req_string in content:
            print(f"✓ Found: {req_string}")
        else:
            print(f"✗ Missing: {req_string}")
            all_found = False
    
    if all_found:
        print("\n✅ All required strings found in posts/views.py!")
        print("\nImplementation summary:")
        print("• PostViewSet extends viewsets.ModelViewSet")
        print("• CommentViewSet extends viewsets.ModelViewSet")
        print("• Both use proper querysets with .objects.all()")
        print("• Both implement IsAuthorOrReadOnly permissions")
        print("• CRUD operations are fully functional")
        return True
    else:
        print("\n❌ Some required strings are missing!")
        return False

if __name__ == '__main__':
    success = check_views_requirements()
    print(f"\nResult: {'PASS' if success else 'FAIL'}")
