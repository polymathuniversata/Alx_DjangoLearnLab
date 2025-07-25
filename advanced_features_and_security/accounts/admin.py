from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
# from .models import CustomUser

'''
class CustomUserAdmin(UserAdmin):
    """
    Custom admin interface for CustomUser model.
    """
    model = CustomUser
    list_display = ('username', 'email', 'first_name', 'last_name', 'date_of_birth', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'date_joined', 'date_of_birth')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('username',)
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Information', {
            'fields': ('date_of_birth', 'profile_photo'),
        }),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Information', {
            'fields': ('date_of_birth', 'profile_photo'),
        }),
    )

# Register the CustomUser model with the custom admin
admin.site.register(CustomUser, CustomUserAdmin)
'''
