from rest_framework import viewsets, permissions, filters, status, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404
from .models import Post, Comment, Like
from .serializers import PostSerializer, PostListSerializer, CommentSerializer
from .permissions import IsAuthorOrReadOnly

User = get_user_model()


class PostViewSet(viewsets.ModelViewSet):
    """ViewSet for managing posts with full CRUD operations using Django REST Framework."""
    
    queryset = Post.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['author']
    search_fields = ['title', 'content']
    ordering_fields = ['created_at', 'updated_at', 'title']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action."""
        if self.action == 'list':
            return PostListSerializer
        return PostSerializer
    
    def get_queryset(self):
        """Filter queryset based on query parameters."""
        queryset = Post.objects.select_related('author').prefetch_related('comments__author')
        
        # Filter by title if provided
        title_query = self.request.query_params.get('title', None)
        if title_query:
            queryset = queryset.filter(title__icontains=title_query)
        
        # Filter by content if provided
        content_query = self.request.query_params.get('content', None)
        if content_query:
            queryset = queryset.filter(content__icontains=content_query)
            
        return queryset
    
    @action(detail=True, methods=['get'])
    def comments(self, request, pk=None):
        """Get all comments for a specific post."""
        post = self.get_object()
        comments = post.comments.select_related('author').order_by('created_at')
        serializer = CommentSerializer(comments, many=True, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def my_posts(self, request):
        """Get posts created by the current user."""
        posts = self.get_queryset().filter(author=request.user)
        page = self.paginate_queryset(posts)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(posts, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        """Like a post."""
        post = self.get_object()
        
        # Check if user already liked this post
        existing_like = Like.objects.filter(post=post, user=request.user).first()
        if existing_like:
            return Response(
                {'message': 'You have already liked this post'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Create like
        like = Like.objects.create(post=post, user=request.user)
        
        # Create notification for post author (if not liking own post)
        if post.author != request.user:
            from notifications.models import Notification
            content_type = ContentType.objects.get_for_model(post)
            Notification.objects.create(
                recipient=post.author,
                actor=request.user,
                verb='liked your post',
                target_content_type=content_type,
                target_object_id=post.id
            )
        
        return Response(
            {'message': 'Post liked successfully'}, 
            status=status.HTTP_201_CREATED
        )
    
    @action(detail=True, methods=['delete'])
    def unlike(self, request, pk=None):
        """Unlike a post."""
        post = self.get_object()
        
        # Check if user has liked this post
        existing_like = Like.objects.filter(post=post, user=request.user).first()
        if not existing_like:
            return Response(
                {'message': 'You have not liked this post'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Delete like
        existing_like.delete()
        
        return Response(
            {'message': 'Post unliked successfully'}, 
            status=status.HTTP_200_OK
        )


class CommentViewSet(viewsets.ModelViewSet):
    """ViewSet for managing comments with full CRUD operations using Django REST Framework."""
    
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['post', 'author']
    search_fields = ['content']
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['created_at']
    
    def perform_create(self, serializer):
        """Override to create notification when comment is created."""
        comment = serializer.save(author=self.request.user)
        
        # Create notification for post author (if not commenting on own post)
        if comment.post.author != self.request.user:
            from notifications.models import Notification
            content_type = ContentType.objects.get_for_model(comment)
            Notification.objects.create(
                recipient=comment.post.author,
                actor=self.request.user,
                verb='commented on your post',
                target_content_type=content_type,
                target_object_id=comment.id
            )
    
    def get_queryset(self):
        """Filter queryset based on query parameters."""
        queryset = Comment.objects.select_related('author', 'post')
        
        # Filter by post if provided
        post_id = self.request.query_params.get('post', None)
        if post_id:
            queryset = queryset.filter(post_id=post_id)
            
        return queryset
    
    @action(detail=False, methods=['get'])
    def my_comments(self, request):
        """Get comments created by the current user."""
        comments = self.get_queryset().filter(author=request.user)
        page = self.paginate_queryset(comments)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(comments, many=True)
        return Response(serializer.data)


class FeedView(generics.ListAPIView):
    """Feed view that shows posts from users that the current user follows."""
    
    serializer_class = PostListSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.OrderingFilter]
    ordering = ['-created_at']
    
    def get_queryset(self):
        """Return posts from users that the current user follows."""
        user = self.request.user
        
        # Get users that the current user follows
        following_users = user.following.all()
        
        # Get posts from those users, ordered by creation date (most recent first)
        queryset = Post.objects.filter(author__in=following_users).order_by('-created_at').select_related('author').prefetch_related('comments__author')
        
        return queryset
        
    def list(self, request, *args, **kwargs):
        """Override list to provide additional context in response."""
        queryset = self.filter_queryset(self.get_queryset())
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        
        # Add additional context
        response_data = {
            'count': queryset.count(),
            'results': serializer.data
        }
        
        return Response(response_data)


class LikePostView(generics.GenericAPIView):
    """View to handle liking a post."""
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, pk):
        """Like a post."""
        post = generics.get_object_or_404(Post, pk=pk)
        
        # Use get_or_create to handle duplicate likes
        like, created = Like.objects.get_or_create(user=request.user, post=post)
        
        if not created:
            return Response(
                {'message': 'You have already liked this post'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Create notification for post author (if not liking own post)
        if post.author != request.user:
            from notifications.models import Notification
            content_type = ContentType.objects.get_for_model(post)
            Notification.objects.create(
                recipient=post.author,
                actor=request.user,
                verb='liked your post',
                target_content_type=content_type,
                target_object_id=post.id
            )
        
        return Response(
            {'message': 'Post liked successfully'}, 
            status=status.HTTP_201_CREATED
        )


class UnlikePostView(generics.GenericAPIView):
    """View to handle unliking a post."""
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, pk):
        """Unlike a post."""
        post = generics.get_object_or_404(Post, pk=pk)
        
        # Check if user has liked this post
        try:
            like = Like.objects.get(post=post, user=request.user)
            like.delete()
            return Response(
                {'message': 'Post unliked successfully'}, 
                status=status.HTTP_200_OK
            )
        except Like.DoesNotExist:
            return Response(
                {'message': 'You have not liked this post'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
