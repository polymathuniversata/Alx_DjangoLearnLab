"""
Development settings for config project.
"""

from .base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-5w^#b#d2gny6_c1k@h49+)yb2*ss#zay-hdbz+a%4lf%zhio*b"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['testserver', 'localhost', '127.0.0.1']

# Database
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# Enable Django debug toolbar for development
INSTALLED_APPS += [
    'django_extensions',
]