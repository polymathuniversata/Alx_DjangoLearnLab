from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Post, Comment, Like

User = get_user_model()


class AuthorSerializer(serializers.ModelSerializer):
    """Serializer for post/comment author information."""
    
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name']
        read_only_fields = ['id', 'username', 'first_name', 'last_name']


class CommentSerializer(serializers.ModelSerializer):
    """Serializer for Comment model."""
    
    author = AuthorSerializer(read_only=True)
    
    class Meta:
        model = Comment
        fields = ['id', 'post', 'author', 'content', 'created_at', 'updated_at']
        read_only_fields = ['id', 'author', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        """Override create to set the author from request user."""
        request = self.context.get('request')
        validated_data['author'] = request.user
        return super().create(validated_data)


class PostSerializer(serializers.ModelSerializer):
    """Serializer for Post model."""
    
    author = AuthorSerializer(read_only=True)
    comment_count = serializers.ReadOnlyField()
    comments = CommentSerializer(many=True, read_only=True)
    likes_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    
    class Meta:
        model = Post
        fields = [
            'id', 'title', 'content', 'author', 'created_at', 
            'updated_at', 'comment_count', 'comments', 'likes_count', 'is_liked'
        ]
        read_only_fields = ['id', 'author', 'created_at', 'updated_at']
    
    def get_likes_count(self, obj):
        """Return the number of likes on this post."""
        return obj.likes.count()
    
    def get_is_liked(self, obj):
        """Check if the current user has liked this post."""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.likes.filter(user=request.user).exists()
        return False
    
    def create(self, validated_data):
        """Override create to set the author from request user."""
        request = self.context.get('request')
        validated_data['author'] = request.user
        return super().create(validated_data)


class PostListSerializer(serializers.ModelSerializer):
    """Serializer for Post list view (without comments to optimize performance)."""
    
    author = AuthorSerializer(read_only=True)
    comment_count = serializers.ReadOnlyField()
    likes_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    
    class Meta:
        model = Post
        fields = [
            'id', 'title', 'content', 'author', 'created_at', 
            'updated_at', 'comment_count', 'likes_count', 'is_liked'
        ]
        read_only_fields = ['id', 'author', 'created_at', 'updated_at']
    
    def get_likes_count(self, obj):
        """Return the number of likes on this post."""
        return obj.likes.count()
    
    def get_is_liked(self, obj):
        """Check if the current user has liked this post."""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.likes.filter(user=request.user).exists()
        return False


class LikeSerializer(serializers.ModelSerializer):
    """Serializer for Like model."""
    
    user = AuthorSerializer(read_only=True)
    
    class Meta:
        model = Like
        fields = ['id', 'post', 'user', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']