#!/usr/bin/env python
"""
Test production settings configuration
"""

import os
import sys
import django
from pathlib import Path

# Add the project directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'social_media_api.settings')
django.setup()

from django.conf import settings
from django.core.management import execute_from_command_line

def test_production_settings():
    """Test that production settings are correctly configured"""
    print("🔍 Testing Production Settings Configuration")
    print("=" * 50)
    
    # Test DEBUG setting
    debug_status = "✅ PASS" if not settings.DEBUG else "❌ FAIL"
    print(f"DEBUG = False: {debug_status} (Current: {settings.DEBUG})")
    
    # Test ALLOWED_HOSTS
    hosts_status = "✅ PASS" if settings.ALLOWED_HOSTS else "❌ FAIL"
    print(f"ALLOWED_HOSTS configured: {hosts_status} (Current: {settings.ALLOWED_HOSTS})")
    
    # Test security settings
    security_checks = {
        'SECURE_BROWSER_XSS_FILTER': getattr(settings, 'SECURE_BROWSER_XSS_FILTER', False),
        'SECURE_CONTENT_TYPE_NOSNIFF': getattr(settings, 'SECURE_CONTENT_TYPE_NOSNIFF', False),
        'X_FRAME_OPTIONS': getattr(settings, 'X_FRAME_OPTIONS', None) == 'DENY',
    }
    
    print("\n🔒 Security Settings:")
    for setting, value in security_checks.items():
        status = "✅ PASS" if value else "❌ FAIL"
        print(f"  {setting}: {status}")
    
    # Test static files configuration
    static_checks = {
        'STATIC_URL': bool(settings.STATIC_URL),
        'STATIC_ROOT': bool(settings.STATIC_ROOT),
        'WhiteNoise in MIDDLEWARE': 'whitenoise.middleware.WhiteNoiseMiddleware' in settings.MIDDLEWARE,
    }
    
    print("\n📁 Static Files Configuration:")
    for setting, value in static_checks.items():
        status = "✅ PASS" if value else "❌ FAIL"
        print(f"  {setting}: {status}")
    
    # Test database configuration
    db_engine = settings.DATABASES['default']['ENGINE']
    db_configured = db_engine != 'django.db.backends.sqlite3' or 'DATABASE_URL' in os.environ
    db_status = "✅ PASS" if db_configured else "⚠️  WARNING"
    print(f"\n🗄️  Database Configuration: {db_status}")
    print(f"  Engine: {db_engine}")
    
    # Overall assessment
    all_critical_pass = (
        not settings.DEBUG and 
        settings.ALLOWED_HOSTS and 
        all(security_checks.values()) and
        all(static_checks.values())
    )
    
    print("\n" + "=" * 50)
    if all_critical_pass:
        print("🎉 All critical production settings are properly configured!")
    else:
        print("⚠️  Some production settings need attention. Review the failures above.")
    
    return all_critical_pass

if __name__ == "__main__":
    test_production_settings()
