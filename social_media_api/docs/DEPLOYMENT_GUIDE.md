# Django Social Media API - Production Deployment Guide

## Overview
This guide covers deploying the Django Social Media API to production using free-tier hosting services. The application is configured with proper security settings, static file handling, and database configurations for production use.

## ✅ Production Configuration Checklist

### ✅ Security Settings Implemented
- `DEBUG = False` - Production safety
- `ALLOWED_HOSTS` configured via environment variables
- `SECURE_BROWSER_XSS_FILTER = True` - XSS protection
- `SECURE_CONTENT_TYPE_NOSNIFF = True` - MIME type sniffing protection  
- `X_FRAME_OPTIONS = 'DENY'` - Clickjacking protection
- `SECURE_SSL_REDIRECT` configurable via environment variables
- HSTS (HTTP Strict Transport Security) enabled
- Secure cookies for HTTPS

### ✅ Database Configuration
- Supports PostgreSQL via `DATABASE_URL` environment variable
- Falls back to individual database settings (`DB_NAME`, `DB_USER`, etc.)
- SQLite fallback for development/testing
- Connection pooling and health checks enabled

### ✅ Static Files & Media
- WhiteNoise middleware for static file serving
- Compressed static files with `CompressedManifestStaticFilesStorage`
- `collectstatic` command integrated in deployment process
- Media files properly configured

## 🚀 Deployment Options

### Option 1: Heroku (Free Tier Alternative - Render)

1. **Setup Render Account**
   - Sign up at [render.com](https://render.com)
   - Connect your GitHub account

2. **Deploy Steps**
   ```bash
   # Push your code to GitHub
   git add .
   git commit -m "Production deployment configuration"
   git push origin main
   ```

3. **Create New Web Service**
   - Select "Web Service" on Render dashboard
   - Connect your GitHub repository
   - Configure settings:
     - **Name**: social-media-api
     - **Region**: Oregon (US West)
     - **Branch**: main
     - **Runtime**: Python 3
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `gunicorn social_media_api.wsgi:application`

4. **Environment Variables**
   ```
   SECRET_KEY=your-generated-secret-key
   DEBUG=False
   ALLOWED_HOSTS=your-app-name.onrender.com
   DATABASE_URL=postgresql://user:pass@hostname:port/dbname
   SECURE_SSL_REDIRECT=true
   ```

### Option 2: Railway (Free Tier)

1. **Setup Railway Account**
   - Sign up at [railway.app](https://railway.app)
   - Connect GitHub account

2. **Deploy Steps**
   ```bash
   # Install Railway CLI
   npm install -g @railway/cli
   
   # Login and deploy
   railway login
   railway link
   railway up
   ```

3. **Environment Variables**
   Set in Railway dashboard or via CLI:
   ```bash
   railway variables set SECRET_KEY=your-secret-key
   railway variables set DEBUG=False
   railway variables set ALLOWED_HOSTS=your-app.railway.app
   ```

### Option 3: PythonAnywhere (Free Tier)

1. **Upload Code**
   - Create account at [pythonanywhere.com](https://pythonanywhere.com)
   - Upload code via Git or file manager

2. **Setup Web App**
   - Create new web app with Django framework
   - Configure WSGI file to point to your application
   - Set environment variables in web app settings

## 🔧 Environment Variables Configuration

Create a `.env` file based on `.env.example`:

```bash
# Required variables
SECRET_KEY=your-super-secret-key-here
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,your-app.onrender.com

# Database (PostgreSQL recommended)
DATABASE_URL=postgresql://user:password@host:port/database

# Security
SECURE_SSL_REDIRECT=true

# Optional: Email settings
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

## 📦 Static Files Management

The application uses WhiteNoise for static file serving:

```bash
# Collect static files
python manage.py collectstatic --noinput

# Files are automatically served by WhiteNoise middleware
# No additional configuration needed for basic deployment
```

## 🗄️ Database Setup

### PostgreSQL (Recommended)
```bash
# On your hosting platform, add PostgreSQL database
# Set DATABASE_URL environment variable
# Run migrations
python manage.py migrate
```

### Free PostgreSQL Options:
- **Render**: Includes free PostgreSQL database
- **Railway**: Free PostgreSQL database included
- **Supabase**: Free PostgreSQL hosting
- **ElephantSQL**: Free tier available

## 🔍 Monitoring & Logging

### Application Logs
- Logs are written to `logs/django.log`
- Console logging enabled for hosting platforms
- Structured logging with timestamps and log levels

### Health Checks
```python
# Add to your views for monitoring
def health_check(request):
    return JsonResponse({'status': 'healthy'})
```

## 🚨 Security Considerations

### SSL/TLS
- Enable `SECURE_SSL_REDIRECT=true` only after confirming HTTPS works
- Most hosting platforms provide automatic SSL certificates

### Secret Key Management
```python
# Generate a new secret key for production
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

### Database Security
- Use strong passwords
- Enable connection encryption
- Limit database access to your application only

## 🧪 Testing Production Settings

Test your production configuration locally:

```bash
# Set environment variables
export DEBUG=False
export SECRET_KEY=your-secret-key
export ALLOWED_HOSTS=localhost,127.0.0.1

# Collect static files
python manage.py collectstatic --noinput

# Run with production settings
python manage.py runserver
```

## 📋 Deployment Checklist

- [ ] `DEBUG = False` in settings
- [ ] `ALLOWED_HOSTS` properly configured
- [ ] Secret key set via environment variable
- [ ] Database configured (PostgreSQL recommended)
- [ ] Static files collected (`collectstatic`)
- [ ] Security settings enabled
- [ ] Environment variables set on hosting platform
- [ ] Database migrations run
- [ ] SSL/HTTPS enabled
- [ ] Monitoring/logging configured

## 🔧 Maintenance & Updates

### Regular Tasks
```bash
# Update dependencies
pip install -r requirements.txt --upgrade

# Run migrations
python manage.py migrate

# Collect static files after updates
python manage.py collectstatic --noinput

# Check for security issues
python manage.py check --deploy
```

### Backup Strategy
- Regular database backups
- Code repository backups (Git)
- Environment variables documentation

## 🆘 Troubleshooting

### Common Issues

1. **Static Files Not Loading**
   ```bash
   python manage.py collectstatic --noinput
   # Ensure WhiteNoise is in MIDDLEWARE
   ```

2. **Database Connection Errors**
   ```bash
   # Check DATABASE_URL format
   # Verify database credentials
   python manage.py dbshell  # Test connection
   ```

3. **500 Internal Server Error**
   ```bash
   # Check logs
   # Verify environment variables
   # Run: python manage.py check --deploy
   ```

4. **CORS Issues**
   ```bash
   # Add django-cors-headers if needed
   pip install django-cors-headers
   ```

## 📚 Additional Resources

- [Django Deployment Checklist](https://docs.djangoproject.com/en/stable/howto/deployment/checklist/)
- [WhiteNoise Documentation](http://whitenoise.evans.io/)
- [Render Django Tutorial](https://render.com/docs/deploy-django)
- [Railway Django Guide](https://docs.railway.app/getting-started)

## 🎯 Next Steps

1. Deploy to your chosen platform
2. Set up monitoring and alerts
3. Configure custom domain (if needed)
4. Implement CI/CD pipeline
5. Set up regular backups
6. Performance optimization

---

**Note**: This configuration prioritizes free-tier deployment options while maintaining production-grade security and performance standards.
