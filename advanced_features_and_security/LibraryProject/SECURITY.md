# Security Measures for LibraryProject

This document summarizes security best practices and configurations implemented in the Django LibraryProject.

## 1. Django Secure Settings
- `DEBUG = False` in production (prevents leaking sensitive info).
- `SECURE_BROWSER_XSS_FILTER = True`: Enables X-XSS-Protection browser header.
- `X_FRAME_OPTIONS = 'DENY'`: Prevents clickjacking.
- `SECURE_CONTENT_TYPE_NOSNIFF = True`: Prevents MIME-type sniffing.
- `CSRF_COOKIE_SECURE = True` and `SESSION_COOKIE_SECURE = True`: Cookies sent only over HTTPS.
- **CSP**: Content Security Policy headers set via `django-csp` middleware to restrict scripts/styles/images to self.

## 2. CSRF Protection
- All forms include `{% csrf_token %}` to prevent CSRF attacks.
- Django's CSRF middleware is enabled by default.

## 3. Safe Data Access
- All database queries use Django ORM (no raw SQL).
- All user input is validated via Django forms or explicit checks in views.
- No user input is directly interpolated into queries.

## 4. Content Security Policy (CSP)
- Configured via `django-csp` middleware in `settings.py`.
- Only allows scripts/styles/images from the application's own domain.
- Can be adjusted for additional static/media/CDN domains as needed.

## 5. Testing & Documentation
- Security settings and rationale are commented in `settings.py`.
- All templates and views are documented for security practices.
- Manual testing: Forms and input fields checked for CSRF and XSS protection.

---
For more details, see comments in `settings.py` and relevant code sections.
