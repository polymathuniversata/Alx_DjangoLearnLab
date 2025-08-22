from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

app_name = 'accounts'

urlpatterns = [
    # Authentication - as required by the task
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.CustomTokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # User profile - as required by the task
    path('profile/', views.UserProfileView.as_view(), name='profile'),
    path('users/<str:username>/', views.UserDetailView.as_view(), name='user_detail'),
    path('change-password/', views.ChangePasswordView.as_view(), name='change_password'),
    
    # Follow/Unfollow - as required by the task
    path('follow/<int:user_id>/', views.FollowUserView.as_view(), name='follow_user'),
    path('unfollow/<int:user_id>/', views.UnfollowUserView.as_view(), name='unfollow_user'),
]
