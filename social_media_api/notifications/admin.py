from django.contrib import admin
from .models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['recipient', 'actor', 'verb', 'timestamp', 'read']
    list_filter = ['timestamp', 'read', 'verb']
    search_fields = ['recipient__username', 'actor__username', 'verb']
    readonly_fields = ['timestamp', 'target_content_type', 'target_object_id']
    ordering = ['-timestamp']
    date_hierarchy = 'timestamp'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('recipient', 'actor', 'target_content_type')
