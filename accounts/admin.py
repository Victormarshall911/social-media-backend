from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_verified', 'is_online', 'created_at']
    list_filter = ['is_verified', 'is_online', 'is_staff', 'is_private', 'created_at']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    ordering = ['-created_at']

    fieldsets = BaseUserAdmin.fieldsets + (
        ('Profile Information', {
            'fields': ('bio', 'profile_picture', 'cover_photo', 'date_of_birth', 'location', 'website', 'phone_number')
        }),
        ('Social Stats', {
            'fields': ('followers_count', 'following_count', 'posts_count')
        }),
        ('Account Settings', {
            'fields': ('is_private', 'is_verified', 'is_online', 'last_seen')
        }),
    )