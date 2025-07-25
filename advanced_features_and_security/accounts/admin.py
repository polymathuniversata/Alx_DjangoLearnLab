from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    """
    Custom admin interface for CustomUser model.
    """
    model = CustomUser

    # Fields to display in the user list view
    list_display = ('username', 'email', 'first_name', 'last_name', 'date_of_birth', 'is_staff', 'is_active')

    # Fields that can be used for filtering in the admin
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'date_joined', 'date_of_birth')

    # Fields that can be searched
    search_fields = ('username', 'email', 'first_name', 'last_name')

    # Ordering of users in the list view
    ordering = ('username',)

    # Fieldsets for the user detail/edit view
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Information', {
            'fields': ('date_of_birth', 'profile_photo'),
        }),
    )

    # Fields to include when adding a new user
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Information', {
            'fields': ('date_of_birth', 'profile_photo'),
        }),
    )


# Register the CustomUser model with the custom admin
admin.site.register(CustomUser, CustomUserAdmin)
