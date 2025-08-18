#!/usr/bin/env python3
"""
Test script to verify authentication functionality.
This script tests the authentication URLs and views.
"""

import requests
import sys

def test_authentication_urls():
    """Test that authentication URLs are accessible."""
    base_url = "http://127.0.0.1:8000/relationship_app"
    
    urls_to_test = [
        f"{base_url}/login/",
        f"{base_url}/register/",
        f"{base_url}/books/",
        f"{base_url}/libraries/",
    ]
    
    print("Testing authentication URLs...")
    
    for url in urls_to_test:
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                print(f"✓ {url} - OK (Status: {response.status_code})")
            else:
                print(f"✗ {url} - Error (Status: {response.status_code})")
        except requests.exceptions.RequestException as e:
            print(f"✗ {url} - Connection Error: {e}")
    
    print("\nAuthentication URL testing completed!")

if __name__ == "__main__":
    test_authentication_urls()
