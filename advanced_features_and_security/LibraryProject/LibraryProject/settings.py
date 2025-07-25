"""
Django settings for LibraryProject project.
Custom user model configuration.

Security best practices: Always review these settings before deploying to production.
"""

AUTH_USER_MODEL = 'bookshelf.CustomUser'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False  # Set to False for production. Use environment variable in real deployments.

# Browser-side protections
SECURE_BROWSER_XSS_FILTER = True  # Enables the X-XSS-Protection header
X_FRAME_OPTIONS = 'DENY'  # Prevents clickjacking by denying framing
SECURE_CONTENT_TYPE_NOSNIFF = True  # Prevents the browser from MIME-sniffing the content type

# Cookies over HTTPS only
CSRF_COOKIE_SECURE = True  # CSRF cookie sent only over HTTPS
SESSION_COOKIE_SECURE = True  # Session cookie sent only over HTTPS

# Content Security Policy (CSP) - requires django-csp middleware
INSTALLED_APPS += ['csp']  # Ensure django-csp is installed
MIDDLEWARE = [
    'csp.middleware.CSPMiddleware',  # Add CSP middleware near the top
    # ...other middleware...
]
CSP_DEFAULT_SRC = ("'self'",)
CSP_SCRIPT_SRC = ("'self'",)
CSP_STYLE_SRC = ("'self'",)
CSP_IMG_SRC = ("'self'",)
# Adjust CSP_* as needed for your static/media/CDN domains

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
