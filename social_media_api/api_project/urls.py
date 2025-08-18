"""
URL configuration for temp_project project.

URLs for the Book API project.
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter
from api.views import BookViewSet, api_root

# The API URLs are now determined automatically by the router.
urlpatterns = [
    # Root URL shows API documentation
    path('', api_root, name='api-root'),
    # Include admin and API URLs
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),  # Include the API URLs from the api app
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # Token authentication endpoint
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
]
