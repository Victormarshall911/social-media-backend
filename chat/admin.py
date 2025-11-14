from django.contrib import admin
from .models import ChatRoom, Message


@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ['id', 'room_type', 'name', 'get_participants', 'created_by', 'created_at']
    list_filter = ['room_type', 'created_at']
    search_fields = ['name', 'participants__username']
    ordering = ['-updated_at']

    def get_participants(self, obj):
        return ", ".join([p.username for p in obj.participants.all()[:3]])

    get_participants.short_description = 'Participants'


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['id', 'sender', 'room', 'message_type', 'content_preview', 'is_read', 'created_at']
    list_filter = ['message_type', 'is_read', 'created_at']
    search_fields = ['sender__username', 'content', 'room__id']
    ordering = ['-created_at']

    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content

    content_preview.short_description = 'Message'