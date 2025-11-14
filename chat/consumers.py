import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from .models import ChatRoom, Message

User = get_user_model()


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = f'chat_{self.room_id}'

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        """Receive message from WebSocket"""
        data = json.loads(text_data)
        message = data.get('message', '')
        user_id = data.get('user_id')
        message_type = data.get('message_type', 'text')

        # Save message to database
        saved_message = await self.save_message(
            user_id,
            self.room_id,
            message,
            message_type
        )

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'user_id': user_id,
                'message_id': saved_message.id,
                'message_type': message_type,
                'created_at': saved_message.created_at.isoformat(),
            }
        )

    async def chat_message(self, event):
        """Receive message from room group"""
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'user_id': event['user_id'],
            'message_id': event['message_id'],
            'message_type': event['message_type'],
            'created_at': event['created_at'],
        }))

    @database_sync_to_async
    def save_message(self, user_id, room_id, content, message_type):
        """Save message to database"""
        user = User.objects.get(id=user_id)
        room = ChatRoom.objects.get(id=room_id)
        message = Message.objects.create(
            sender=user,
            room=room,
            content=content,
            message_type=message_type
        )
        return message