from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from .models import Notification
from .serializers import NotificationSerializer

User = get_user_model()


class NotificationListView(generics.ListAPIView):
    """List all notifications for the current user."""
    
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Return notifications for the current user, ordered by timestamp."""
        return Notification.objects.filter(
            recipient=self.request.user
        ).select_related('actor', 'target_content_type')


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def mark_notification_read(request, pk):
    """Mark a specific notification as read."""
    try:
        notification = Notification.objects.get(pk=pk, recipient=request.user)
        notification.read = True
        notification.save()
        return Response({'message': 'Notification marked as read'})
    except Notification.DoesNotExist:
        return Response(
            {'error': 'Notification not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def mark_all_notifications_read(request):
    """Mark all notifications for the current user as read."""
    notifications = Notification.objects.filter(
        recipient=request.user, 
        read=False
    )
    notifications.update(read=True)
    return Response({
        'message': f'{notifications.count()} notifications marked as read'
    })


def create_notification(recipient, actor, verb, target_object):
    """Helper function to create notifications."""
    if recipient != actor:  # Don't create notifications for own actions
        content_type = ContentType.objects.get_for_model(target_object)
        Notification.objects.create(
            recipient=recipient,
            actor=actor,
            verb=verb,
            target_content_type=content_type,
            target_object_id=target_object.id
        )
