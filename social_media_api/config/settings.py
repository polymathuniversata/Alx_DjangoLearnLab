"""
Django settings loader for config project.
Automatically loads the appropriate settings module based on environment.
"""

import os

# Determine which settings to use
environment = os.environ.get('DJANGO_ENVIRONMENT', 'development')

if environment == 'production':
    from .settings.production import *
elif environment == 'development':
    from .settings.development import *
else:
    from .settings.development import *
