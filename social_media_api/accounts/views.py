from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model
from .serializers import (
    UserSerializer, 
    RegisterSerializer, 
    CustomTokenObtainPairSerializer,
    ChangePasswordSerializer
)
from rest_framework.permissions import IsAuthenticated

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    """Register a new user."""
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer


class CustomTokenObtainPairView(TokenObtainPairView):
    """Custom token obtain view with additional user data in the response."""
    serializer_class = CustomTokenObtainPairSerializer


class UserProfileView(generics.RetrieveUpdateAPIView):
    """Retrieve or update user profile."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class ChangePasswordView(generics.UpdateAPIView):
    """Change user password."""
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response(
                    {"old_password": ["Wrong password."]},
                    status=status.HTTP_400_BAD_REQUEST
                )
            # Set new password
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }
            return Response(response)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetailView(generics.RetrieveAPIView):
    """Retrieve a user's public profile."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = 'username'


class FollowUserView(APIView):
    """Follow a user."""
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id, *args, **kwargs):
        try:
            user_to_follow = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response(
                {"detail": "User not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )

        if request.user == user_to_follow:
            return Response(
                {"detail": "You cannot follow yourself"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        if user_to_follow in request.user.followers.all():
            return Response(
                {"detail": f"You are already following {user_to_follow.username}"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Follow
        request.user.followers.add(user_to_follow)
        
        # Create notification for the followed user
        from notifications.views import create_notification
        create_notification(
            recipient=user_to_follow,
            actor=request.user,
            verb='started following you',
            target_object=request.user
        )
        
        return Response(
            {"status": "followed", "detail": f"You are now following {user_to_follow.username}"},
            status=status.HTTP_201_CREATED
        )


class UnfollowUserView(APIView):
    """Unfollow a user."""
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id, *args, **kwargs):
        try:
            user_to_unfollow = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response(
                {"detail": "User not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )

        if request.user == user_to_unfollow:
            return Response(
                {"detail": "You cannot unfollow yourself"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        if user_to_unfollow not in request.user.followers.all():
            return Response(
                {"detail": f"You are not following {user_to_unfollow.username}"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Unfollow
        request.user.followers.remove(user_to_unfollow)
        return Response(
            {"status": "unfollowed", "detail": f"You have unfollowed {user_to_unfollow.username}"},
            status=status.HTTP_200_OK
        )
