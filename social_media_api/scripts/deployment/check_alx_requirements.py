#!/usr/bin/env python
"""
ALX Task 4 Requirements Verification Script
"""

import os
import sys
import django
from pathlib import Path

# Setup Django
sys.path.insert(0, str(Path(__file__).parent))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'social_media_api.settings')
django.setup()

from django.conf import settings

def check_alx_requirements():
    """Check all ALX Task 4 requirements"""
    print('🔍 CHECKING ALX TASK 4 REQUIREMENTS')
    print('=' * 50)

    # Check 1: DEBUG = False
    debug_check = not settings.DEBUG
    print(f'✅ DEBUG = False: {debug_check} (Current: {settings.DEBUG})')

    # Check 2: ALLOWED_HOSTS configured  
    hosts_check = bool(settings.ALLOWED_HOSTS)
    print(f'✅ ALLOWED_HOSTS configured: {hosts_check} (Current: {settings.ALLOWED_HOSTS})')

    # Check 3: Security settings
    security_checks = {
        'SECURE_BROWSER_XSS_FILTER': getattr(settings, 'SECURE_BROWSER_XSS_FILTER', False),
        'X_FRAME_OPTIONS': getattr(settings, 'X_FRAME_OPTIONS', None) == 'DENY', 
        'SECURE_CONTENT_TYPE_NOSNIFF': getattr(settings, 'SECURE_CONTENT_TYPE_NOSNIFF', False),
        'SECURE_SSL_REDIRECT': hasattr(settings, 'SECURE_SSL_REDIRECT'),
    }

    print('\n🔒 Security Settings:')
    for setting, value in security_checks.items():
        status = '✅' if value else '❌'
        print(f'  {status} {setting}: {value}')

    # Check 4: Static files with collectstatic
    static_checks = {
        'STATIC_URL': bool(settings.STATIC_URL),
        'STATIC_ROOT': bool(settings.STATIC_ROOT),
        'WhiteNoise': 'whitenoise.middleware.WhiteNoiseMiddleware' in settings.MIDDLEWARE,
        'STATICFILES_STORAGE': hasattr(settings, 'STATICFILES_STORAGE'),
    }

    print('\n📁 Static Files Configuration:')
    for setting, value in static_checks.items():
        status = '✅' if value else '❌'
        print(f'  {status} {setting}: {value}')

    # Check 5: Database credentials setup
    db_config = settings.DATABASES['default']
    db_supports_prod = db_config['ENGINE'] != 'django.db.backends.sqlite3' or 'DATABASE_URL' in os.environ
    db_status = '✅' if db_supports_prod else '⚠️'
    print(f'\n🗄️ Database Configuration: {db_status} (Engine: {db_config["ENGINE"]})')

    # Overall status
    all_critical = (debug_check and hosts_check and 
                   all(security_checks.values()) and 
                   all(static_checks.values()))
    
    overall_status = '✅ COMPLETE' if all_critical else '⚠️ NEEDS ATTENTION'
    print(f'\n🎯 Overall Task 4 Status: {overall_status}')

    # Summary
    print('\n' + '=' * 50)
    print('📋 REQUIREMENTS SUMMARY:')
    print(f'  Production Settings: {"✅" if debug_check and hosts_check else "❌"}')
    print(f'  Security Settings: {"✅" if all(security_checks.values()) else "❌"}')
    print(f'  Static Files Setup: {"✅" if all(static_checks.values()) else "❌"}')
    print(f'  Database Ready: {"✅" if db_supports_prod else "⚠️"}')
    
    return all_critical

if __name__ == "__main__":
    success = check_alx_requirements()
    sys.exit(0 if success else 1)
