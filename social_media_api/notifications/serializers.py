from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Notification

User = get_user_model()


class ActorSerializer(serializers.ModelSerializer):
    """Serializer for the actor field in notifications."""
    
    class Meta:
        model = User
        fields = ['id', 'username', 'profile_picture']


class NotificationSerializer(serializers.ModelSerializer):
    """Serializer for notifications."""
    
    actor = ActorSerializer(read_only=True)
    target_url = serializers.SerializerMethodField()
    time_since = serializers.SerializerMethodField()
    
    class Meta:
        model = Notification
        fields = [
            'id', 'actor', 'verb', 'target_url', 
            'timestamp', 'time_since', 'read'
        ]
        read_only_fields = ['id', 'timestamp']
    
    def get_target_url(self, obj):
        """Get URL for the notification target."""
        if hasattr(obj.target, 'id'):
            if obj.target.__class__.__name__ == 'Post':
                return f'/api/posts/{obj.target.id}/'
            elif obj.target.__class__.__name__ == 'Comment':
                return f'/api/posts/{obj.target.post.id}/comments/{obj.target.id}/'
            elif obj.target.__class__.__name__ == 'CustomUser':
                return f'/api/users/{obj.target.username}/'
        return None
    
    def get_time_since(self, obj):
        """Get human-readable time since notification was created."""
        from django.utils.timesince import timesince
        return timesince(obj.timestamp)