# Social Media API

A RESTful API for a social media platform built with Django and Django REST Framework.

## Features

- User registration and authentication with JWT
- User profiles with bio, profile pictures, and more
- Follow/Unfollow functionality
- Secure password management
- RESTful API design

## Prerequisites

- Python 3.8+
- pip (Python package manager)
- Virtual environment (recommended)

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd social_media_api
   ```

2. Create and activate a virtual environment:
   ```bash
   # On Windows
   python -m venv venv
   .\venv\Scripts\activate
   
   # On macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Apply migrations:
   ```bash
   python manage.py migrate
   ```

5. Create a superuser (admin):
   ```bash
   python manage.py createsuperuser
   ```

6. Run the development server:
   ```bash
   python manage.py runserver
   ```

## API Endpoints

### Authentication

- `POST /api/auth/register/` - Register a new user
- `POST /api/auth/token/` - Obtain JWT token (login)
- `POST /api/auth/token/refresh/` - Refresh JWT token

### User Profile

- `GET /api/auth/profile/` - Get or update current user's profile
- `GET /api/auth/users/<username>/` - Get a user's public profile
- `POST /api/auth/change-password/` - Change password
- `POST /api/auth/follow/<username>/` - Follow/Unfollow a user

## Testing the API

You can use tools like [Postman](https://www.postman.com/) or [curl](https://curl.se/) to test the API endpoints.

### Example: Register a new user

```bash
curl -X POST http://127.0.0.1:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "testpass123",
    "password2": "testpass123",
    "first_name": "Test",
    "last_name": "User"
  }'
```

### Example: Get JWT token

```bash
curl -X POST http://127.0.0.1:8000/api/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "testpass123"}'
```

## Project Structure

```
social_media_api/
├── accounts/                 # User accounts app
│   ├── migrations/           # Database migrations
│   ├── __init__.py
│   ├── admin.py             # Admin interface configuration
│   ├── apps.py              # App configuration
│   ├── models.py            # User and related models
│   ├── serializers.py       # API serializers
│   ├── urls.py             # App URL configuration
│   └── views.py            # API views
├── config/                  # Project configuration
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py         # Project settings
│   ├── urls.py            # Main URL configuration
│   └── wsgi.py
├── media/                  # User-uploaded files (profile pictures)
├── manage.py              # Django management script
└── README.md              # This file
```

## Contributing

1. Fork the repository
2. Create a new branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
