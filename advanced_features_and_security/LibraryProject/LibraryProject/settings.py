"""
Django settings for LibraryProject project.
Custom user model configuration.
"""

AUTH_USER_MODEL = 'bookshelf.CustomUser'

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'bookshelf',
    # ...other apps...
]
