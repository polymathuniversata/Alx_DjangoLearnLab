# Social Media API

A production-ready RESTful API for a social media platform built with Django and Django REST Framework.

## 📁 Project Structure

```
social_media_api/
├── accounts/               # User authentication and profiles
├── posts/                  # Posts and comments functionality  
├── notifications/          # Notification system
├── social_media_api/       # Main Django project settings
├── deployment/             # Deployment configuration files
├── docs/                   # Project documentation
├── scripts/                # Utility and validation scripts
├── logs/                   # Application logs
├── staticfiles/            # Collected static files
├── manage.py              # Django management script
├── requirements.txt       # Project dependencies
├── .env.example           # Environment variables template
└── README.md              # This file
```

## 🚀 Features

### ✅ Task 0: Project Setup & User Authentication
- Custom user model with bio, profile picture, and followers
- JWT token authentication
- User registration, login, and profile management
- Token-based API access

### ✅ Task 1: Posts and Comments Functionality  
- Create, read, update, delete posts
- Comment system on posts
- Pagination and filtering
- User permissions and ownership validation

### ✅ Task 2: User Follows and Feed Functionality
- Follow/unfollow other users
- Personalized feed from followed users
- User relationship management

### ✅ Task 3: Notifications and Likes Functionality
- Like/unlike posts
- Notification system for interactions
- Real-time notifications for follows, likes, comments

### ✅ Task 4: Production Deployment
- Production-ready configuration
- Security settings (XSS, CSRF, HSTS)
- Static file handling with WhiteNoise
- Multiple hosting platform support
- Environment-based configuration

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- Virtual environment (recommended)

### Local Development Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/Alx_DjangoLearnLab.git
   cd Alx_DjangoLearnLab/social_media_api
   ```

2. **Create and activate virtual environment:**
   ```bash
   # Windows
   python -m venv venv
   .\venv\Scripts\activate
   
   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Setup environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Run migrations:**
   ```bash
   python manage.py migrate
   ```

6. **Create superuser:**
   ```bash
   python manage.py createsuperuser
   ```

7. **Start development server:**
   ```bash
   python manage.py runserver
   ```

## 🌐 API Endpoints

### Authentication (`/api/auth/`)
- `POST /api/auth/register/` - User registration
- `POST /api/auth/login/` - User login  
- `POST /api/auth/logout/` - User logout

### User Management (`/api/accounts/`)
- `GET /api/accounts/profile/` - Get user profile
- `PUT /api/accounts/profile/` - Update user profile
- `POST /api/accounts/follow/{user_id}/` - Follow user
- `DELETE /api/accounts/unfollow/{user_id}/` - Unfollow user

### Posts (`/api/posts/`)
- `GET /api/posts/` - List all posts (paginated)
- `POST /api/posts/` - Create new post
- `GET /api/posts/{id}/` - Get specific post
- `PUT /api/posts/{id}/` - Update post (owner only)
- `DELETE /api/posts/{id}/` - Delete post (owner only)

### Comments (`/api/posts/{post_id}/comments/`)
- `GET /api/posts/{post_id}/comments/` - List post comments
- `POST /api/posts/{post_id}/comments/` - Add comment
- `PUT /api/comments/{id}/` - Update comment (owner only)
- `DELETE /api/comments/{id}/` - Delete comment (owner only)

### Likes (`/api/posts/{post_id}/`)
- `POST /api/posts/{post_id}/like/` - Like post
- `DELETE /api/posts/{post_id}/like/` - Unlike post

### Feed (`/api/feed/`)
- `GET /api/feed/` - Get personalized feed

### Notifications (`/api/notifications/`)
- `GET /api/notifications/` - Get user notifications
- `POST /api/notifications/{id}/read/` - Mark notification as read

## 🚀 Production Deployment

The API is configured for deployment on multiple platforms:

### Render.com (Recommended)
1. Connect your GitHub repository
2. Set environment variables
3. Deploy automatically

### Railway.app
```bash
railway login
railway link
railway up
```

### Docker
```bash
cd deployment/
docker-compose up --build
```

See `docs/DEPLOYMENT_GUIDE.md` for detailed deployment instructions.

## 🔐 Environment Variables

Required environment variables:

```bash
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,your-app.herokuapp.com

# Database
DATABASE_URL=postgresql://user:password@host:port/database

# Security
SECURE_SSL_REDIRECT=true
```

## 🧪 Testing

Run the test suite:
```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test accounts
python manage.py test posts
python manage.py test notifications

# Run deployment checks
python scripts/deployment/check_alx_requirements.py
```

## 📚 Documentation

- `docs/API_DOCUMENTATION.md` - Complete API documentation
- `docs/DEPLOYMENT_GUIDE.md` - Production deployment guide
- `docs/IMPLEMENTATION_SUMMARY.md` - Technical implementation details

## 🛠️ Development Tools

- `scripts/deployment/` - Deployment utilities
- `scripts/validation/` - Testing and validation scripts
- `logs/` - Application logs
- `deployment/` - Platform-specific configurations

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests
5. Submit a pull request

## 📝 License

This project is part of the ALX Software Engineering program.

## 🎯 Learning Objectives Achieved

- ✅ Django project setup and user authentication
- ✅ Posts and comments functionality
- ✅ User follows and feed functionality  
- ✅ Notifications and likes functionality
- ✅ Production deployment configuration

## 📞 Support

For issues and questions:
1. Check the documentation in `docs/`
2. Review the API documentation
3. Check deployment guides for hosting issues

---

**Built with Django REST Framework for the ALX Software Engineering Program**

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
=======
# Alx_DjangoLearnLab
>>>>>>> origin/main
