"""
URL configuration for advanced_api_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.documentation import include_docs_urls

# API URL patterns
urlpatterns = [
    # Admin site
    path('admin/', admin.site.urls),
    
    # API endpoints
    path('api/', include('api.urls')),
    
    # API documentation
    path('api/docs/', include_docs_urls(
        title='Advanced API Project',
        description='A RESTful API for managing authors and books',
        public=True
    )),
    
    # API authentication (for the browsable API)
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
