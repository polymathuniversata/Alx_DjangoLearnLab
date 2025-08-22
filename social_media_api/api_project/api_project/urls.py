"""
URL configuration for the Social Media API project.
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

# The API URLs are now determined automatically by the router.
urlpatterns = [
    # Admin URL
    path('admin/', admin.site.urls),
    
    # API Authentication URLs
    path('api/accounts/', include('accounts.urls')),  # Include accounts app URLs
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    
    # Include other apps' URLs
    path('api/', include('api.urls')),  # Include the API URLs from the api app
    
    # API Authentication (browsable API)
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
