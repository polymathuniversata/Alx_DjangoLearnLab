from django.contrib import admin
from .models import Post, Comment, Like


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'created_at', 'updated_at', 'comment_count']
    list_filter = ['created_at', 'updated_at', 'author']
    search_fields = ['title', 'content', 'author__username']
    readonly_fields = ['created_at', 'updated_at', 'comment_count']
    ordering = ['-created_at']
    date_hierarchy = 'created_at'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'author', 'post', 'created_at', 'updated_at']
    list_filter = ['created_at', 'updated_at', 'author', 'post']
    search_fields = ['content', 'author__username', 'post__title']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']
    date_hierarchy = 'created_at'


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ['user', 'post', 'created_at']
    list_filter = ['created_at', 'user', 'post']
    search_fields = ['user__username', 'post__title']
    readonly_fields = ['created_at']
    ordering = ['-created_at']
