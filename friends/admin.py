from django.contrib import admin
from .models import Friendship, Follow


@admin.register(Friendship)
class FriendshipAdmin(admin.ModelAdmin):
    list_display = ['id', 'from_user', 'to_user', 'status', 'created_at', 'updated_at']
    list_filter = ['status', 'created_at']
    search_fields = ['from_user__username', 'to_user__username']
    ordering = ['-created_at']

    actions = ['accept_requests', 'reject_requests']

    def accept_requests(self, request, queryset):
        for friendship in queryset:
            friendship.accept()
        self.message_user(request, f'{queryset.count()} friend requests accepted.')

    accept_requests.short_description = 'Accept selected friend requests'

    def reject_requests(self, request, queryset):
        for friendship in queryset:
            friendship.reject()
        self.message_user(request, f'{queryset.count()} friend requests rejected.')

    reject_requests.short_description = 'Reject selected friend requests'


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):    list_filter = ['created_at']
