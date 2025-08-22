from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, CommentViewSet, FeedView

# Create a router and register our viewsets with it
router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='posts')
router.register(r'comments', CommentViewSet, basename='comments')

# The API URLs are now determined automatically by the router
urlpatterns = [
    path('', include(router.urls)),
    # Feed endpoint - as required by the task
    path('feed/', FeedView.as_view(), name='feed'),
]