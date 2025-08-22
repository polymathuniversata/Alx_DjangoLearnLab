from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CommentViewSet

# Create a router and register our comments viewset
router = DefaultRouter()
router.register(r'', CommentViewSet, basename='comments')

# The API URLs for comments
urlpatterns = [
    path('', include(router.urls)),
]
