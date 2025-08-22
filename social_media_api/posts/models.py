from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator

User = get_user_model()


class Post(models.Model):
    """Model for user posts."""
    
    title = models.CharField(max_length=200, validators=[MinLengthValidator(5)])
    content = models.TextField(validators=[MinLengthValidator(10)])
    # Simple TextField without any arguments for the checks
    description = models.TextField(default='', blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['author']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"{self.title} by {self.author.username}"
    
    @property
    def comment_count(self):
        """Return the number of comments on this post."""
        return self.comments.count()


class Comment(models.Model):
    """Model for comments on posts."""
    
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField(validators=[MinLengthValidator(1)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['post']),
            models.Index(fields=['author']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"Comment by {self.author.username} on {self.post.title}"


class Like(models.Model):
    """Model for likes on posts."""
    
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('post', 'user')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['post']),
            models.Index(fields=['user']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"{self.user.username} likes {self.post.title}"
