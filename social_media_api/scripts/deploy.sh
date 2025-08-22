#!/bin/bash

# Deployment script for Social Media API
set -e

echo "Starting deployment..."

# Set environment variables
export DJANGO_ENVIRONMENT=production

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Run migrations
echo "Running database migrations..."
python manage.py migrate

# Create superuser if it doesn't exist
echo "Creating superuser (if needed)..."
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin_password_change_me')
    print('Superuser created')
else:
    print('Superuser already exists')
"

echo "Deployment completed successfully!"

# Start the server
echo "Starting server..."
gunicorn config.wsgi:application --config gunicorn.conf.py