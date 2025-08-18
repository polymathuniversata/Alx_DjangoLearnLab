from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

app_name = 'accounts'

urlpatterns = [
    # Authentication
    path('register/', views.RegisterView.as_view(), name='register'),
    path('token/', views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # User profile
    path('profile/', views.UserProfileView.as_view(), name='profile'),
    path('users/<str:username>/', views.UserDetailView.as_view(), name='user_detail'),
    path('change-password/', views.ChangePasswordView.as_view(), name='change_password'),
    
    # Follow/Unfollow
    path('follow/<str:username>/', views.FollowUserView.as_view(), name='follow_user'),
]
