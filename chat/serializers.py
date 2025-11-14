from rest_framework import serializers
from .models import ChatRoom, Message
from accounts.serializers import UserMinimalSerializer  # Changed from relative import

class MessageSerializer(serializers.ModelSerializer):
    """Serializer for Message model"""
    sender = UserMinimalSerializer(read_only=True)

    class Meta:
        model = Message
        fields = [
            'id', 'room', 'sender', 'message_type', 'content',
            'file', 'is_read', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'sender', 'is_read', 'created_at', 'updated_at']


class ChatRoomSerializer(serializers.ModelSerializer):
    """Serializer for ChatRoom model"""
    participants = UserMinimalSerializer(many=True, read_only=True)
    created_by = UserMinimalSerializer(read_only=True)
    last_message = serializers.SerializerMethodField()
    unread_count = serializers.SerializerMethodField()

    class Meta:
        model = ChatRoom
        fields = [
            'id', 'room_type', 'name', 'participants',
            'created_by', 'last_message', 'unread_count',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_by', 'created_at', 'updated_at']

    def get_last_message(self, obj):
        last_msg = obj.messages.last()
        if last_msg:
            return MessageSerializer(last_msg).data
        return None

    def get_unread_count(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.messages.exclude(read_by=request.user).count()
        return 0