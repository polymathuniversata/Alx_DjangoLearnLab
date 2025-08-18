# Authentication System

This document describes the authentication system for the Django Blog.

## Features
- Login and Logout using Django's built-in auth views.
- Registration using a custom `RegistrationForm` extending `UserCreationForm` (adds email, optional first/last name).
- Profile view to update email, first name, last name for the currently logged-in user.

## Key Files
- `blog/forms.py`: `RegistrationForm`, `ProfileForm`
- `blog/views.py`: `home`, `register`, `profile`
- `blog/urls.py`: URL patterns for home, login, logout, register, profile
- Templates under `blog/templates/blog/`: `base.html`, `home.html`, `login.html`, `logged_out.html`, `register.html`, `profile.html`
- `django_blog/settings.py`: `LOGIN_REDIRECT_URL`, `LOGOUT_REDIRECT_URL`, `LOGIN_URL`

## URLs
- `/` — Home page
- `/login/` — Login
- `/logout/` — Logout
- `/register/` — Create account
- `/profile/` — View/edit profile (login required)

## Testing
1. Visit `/register/`, create a user.
2. After success, you are prompted to login at `/login/`.
3. On login, you will be redirected to `/`.
4. Visit `/profile/` to edit your details and save.
5. Click `Logout` to end your session. You will be redirected to `/`.

## Security
- CSRF protection is applied on all forms via `{% csrf_token %}`.
- Passwords are handled via Django's built-in hashing and validators.
- Profile route is protected by `@login_required`.
