# Deployment Guide - Social Media API

This guide provides comprehensive instructions for deploying the Django Social Media API to various production environments.

## 📋 Prerequisites

- Python 3.11+
- PostgreSQL 12+ (for production database)
- Git
- A hosting account (Heroku, AWS, DigitalOcean, etc.)

## 🏗️ Project Structure

```
social_media_api/
├── config/
│   ├── settings/
│   │   ├── base.py          # Base settings
│   │   ├── development.py   # Development settings
│   │   └── production.py    # Production settings
│   └── wsgi.py
├── scripts/
│   ├── deploy.sh           # Deployment script
│   └── setup_postgres.py   # Database setup
├── .env.example           # Environment variables template
├── Procfile              # Heroku process file
├── runtime.txt           # Python version
├── gunicorn.conf.py      # Gunicorn configuration
├── Dockerfile            # Docker configuration
├── docker-compose.yml    # Docker Compose
├── nginx.conf            # Nginx configuration
└── requirements.txt      # Python dependencies
```

## 🔧 Configuration Steps

### 1. Environment Variables Setup

Copy the environment template and configure your production values:

```bash
cp .env.example .env
```

Edit `.env` with your production values:
- `SECRET_KEY`: Generate a new secret key
- `DJANGO_ENVIRONMENT`: Set to "production"
- `ALLOWED_HOSTS`: Your domain names
- `DATABASE_URL` or individual DB settings
- Other service credentials as needed

### 2. Database Configuration

For PostgreSQL, you can use the provided setup script:

```bash
python scripts/setup_postgres.py
```

Or manually create:
```sql
CREATE DATABASE social_media_api;
CREATE USER social_media_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE social_media_api TO social_media_user;
```

## 🚀 Deployment Options

### Option 1: Heroku Deployment

#### Quick Deploy Button
[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/polymathuniversata/Alx_DjangoLearnLab)

#### Manual Heroku Deployment

1. **Install Heroku CLI**
   ```bash
   # Install Heroku CLI (if not already installed)
   # https://devcenter.heroku.com/articles/heroku-cli
   ```

2. **Login and Create App**
   ```bash
   heroku login
   heroku create your-app-name
   ```

3. **Set Environment Variables**
   ```bash
   heroku config:set SECRET_KEY="your-secret-key"
   heroku config:set DJANGO_ENVIRONMENT=production
   heroku config:set ALLOWED_HOSTS=".herokuapp.com"
   ```

4. **Add PostgreSQL Database**
   ```bash
   heroku addons:create heroku-postgresql:mini
   ```

5. **Deploy**
   ```bash
   git add .
   git commit -m "Ready for deployment"
   git push heroku main
   ```

6. **Run Migrations**
   ```bash
   heroku run python manage.py migrate
   heroku run python manage.py createsuperuser
   ```

### Option 2: DigitalOcean Deployment

1. **Create Droplet**
   - Ubuntu 22.04 LTS
   - Minimum 1GB RAM

2. **Server Setup**
   ```bash
   # Update system
   sudo apt update && sudo apt upgrade -y
   
   # Install required packages
   sudo apt install python3 python3-pip python3-venv postgresql postgresql-contrib nginx -y
   
   # Create application user
   sudo adduser --disabled-password --gecos '' appuser
   ```

3. **Database Setup**
   ```bash
   sudo -u postgres createdb social_media_api
   sudo -u postgres createuser social_media_user
   sudo -u postgres psql -c "ALTER USER social_media_user WITH PASSWORD 'your_password';"
   sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE social_media_api TO social_media_user;"
   ```

4. **Application Deployment**
   ```bash
   sudo -u appuser -i
   git clone https://github.com/polymathuniversata/Alx_DjangoLearnLab.git
   cd Alx_DjangoLearnLab/social_media_api
   
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   
   # Configure environment
   cp .env.example .env
   # Edit .env with your values
   
   # Run migrations
   python manage.py migrate
   python manage.py collectstatic
   python manage.py createsuperuser
   ```

5. **Configure Systemd Service**
   ```bash
   sudo nano /etc/systemd/system/social-media-api.service
   ```
   
   Add the service configuration:
   ```ini
   [Unit]
   Description=Social Media API
   After=network.target
   
   [Service]
   User=appuser
   Group=www-data
   WorkingDirectory=/home/appuser/Alx_DjangoLearnLab/social_media_api
   ExecStart=/home/appuser/Alx_DjangoLearnLab/social_media_api/venv/bin/gunicorn config.wsgi:application --config gunicorn.conf.py
   Restart=always
   
   [Install]
   WantedBy=multi-user.target
   ```

6. **Configure Nginx**
   ```bash
   sudo cp nginx.conf /etc/nginx/sites-available/social-media-api
   sudo ln -s /etc/nginx/sites-available/social-media-api /etc/nginx/sites-enabled/
   sudo nginx -t
   sudo systemctl restart nginx
   ```

### Option 3: Docker Deployment

1. **Build and Run**
   ```bash
   docker-compose up --build -d
   ```

2. **Run Migrations**
   ```bash
   docker-compose exec web python manage.py migrate
   docker-compose exec web python manage.py createsuperuser
   ```

### Option 4: AWS Elastic Beanstalk

1. **Install EB CLI**
   ```bash
   pip install awsebcli
   ```

2. **Initialize and Deploy**
   ```bash
   eb init -p python-3.11 social-media-api
   eb create production
   eb setenv SECRET_KEY="your-secret-key" DJANGO_ENVIRONMENT=production
   eb deploy
   ```

## 🔒 Security Checklist

- [ ] `DEBUG = False` in production
- [ ] Strong `SECRET_KEY` generated
- [ ] `ALLOWED_HOSTS` properly configured
- [ ] Database credentials secured
- [ ] HTTPS configured
- [ ] Security headers enabled
- [ ] Static/media files properly served
- [ ] Regular backups scheduled

## 📊 Monitoring and Maintenance

### Health Check Endpoints
- `/admin/` - Django admin
- `/api/` - API root

### Logs
- Application logs: Check your hosting platform's log system
- Database logs: Monitor PostgreSQL logs
- Web server logs: Monitor Nginx/Apache logs

### Regular Maintenance
1. **Database Backups**
   ```bash
   pg_dump social_media_api > backup_$(date +%Y%m%d).sql
   ```

2. **Dependency Updates**
   ```bash
   pip list --outdated
   pip install -r requirements.txt --upgrade
   ```

3. **Security Updates**
   ```bash
   sudo apt update && sudo apt upgrade -y
   ```

## 🐛 Troubleshooting

### Common Issues

1. **Static Files Not Loading**
   - Check `STATIC_ROOT` and `STATICFILES_STORAGE` settings
   - Run `python manage.py collectstatic`

2. **Database Connection Issues**
   - Verify database credentials
   - Check firewall settings
   - Ensure PostgreSQL is running

3. **Permission Errors**
   - Check file/directory permissions
   - Ensure proper user ownership

4. **Memory Issues**
   - Monitor server resources
   - Adjust Gunicorn worker count
   - Consider upgrading server specs

### Debug Commands

```bash
# Check deployment configuration
python manage.py check --deploy

# Test database connection
python manage.py dbshell

# Check static files
python manage.py collectstatic --dry-run

# View logs
heroku logs --tail  # For Heroku
docker-compose logs web  # For Docker
```

## 🌐 Post-Deployment

1. **Test API Endpoints**
   ```bash
   curl https://your-domain.com/api/
   ```

2. **Create Initial Data**
   - Create superuser account
   - Set up initial data if needed

3. **Configure Monitoring**
   - Set up application monitoring
   - Configure error tracking
   - Set up uptime monitoring

## 📞 Support

For deployment issues:
1. Check the troubleshooting section above
2. Review Django deployment documentation
3. Check your hosting provider's documentation
4. Review application logs for specific errors

---

**Live URL**: `https://your-deployed-app.herokuapp.com`  
**Admin Panel**: `https://your-deployed-app.herokuapp.com/admin/`  
**API Root**: `https://your-deployed-app.herokuapp.com/api/`