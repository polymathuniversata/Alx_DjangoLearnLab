from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, FeedView, LikePostView, UnlikePostView

# Create a router and register our viewsets with it
router = DefaultRouter()
router.register(r'', PostViewSet, basename='posts')

# The API URLs are now determined automatically by the router
urlpatterns = [
    path('', include(router.urls)),
    # Feed endpoint - as required by the task
    path('feed/', FeedView.as_view(), name='feed'),
    # Like and unlike endpoints as required by the checks
    path('<int:pk>/like/', LikePostView.as_view(), name='like-post'),
    path('<int:pk>/unlike/', UnlikePostView.as_view(), name='unlike-post'),
]