from django.db import models
from django.conf import settings


class ChatRoom(models.Model):
    """Chat room for conversations"""
    ROOM_TYPE_CHOICES = (
        ('direct', 'Direct Message'),
        ('group', 'Group Chat'),
    )

    room_type = models.CharField(
        max_length=10,
        choices=ROOM_TYPE_CHOICES,
        default='direct'
    )
    name = models.CharField(max_length=100, blank=True)  # For group chats
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='chat_rooms'
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_rooms'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        if self.room_type == 'direct':
            participants = list(self.participants.all()[:2])
            if len(participants) == 2:
                return f"{participants[0].username} & {participants[1].username}"
        return self.name or f"Room {self.id}"


class Message(models.Model):
    """Message model for chat"""
    MESSAGE_TYPE_CHOICES = (
        ('text', 'Text'),
        ('image', 'Image'),
        ('video', 'Video'),
        ('file', 'File'),
    )

    room = models.ForeignKey(
        ChatRoom,
        on_delete=models.CASCADE,
        related_name='messages'
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sent_messages'
    )
    message_type = models.CharField(
        max_length=10,
        choices=MESSAGE_TYPE_CHOICES,
        default='text'
    )
    content = models.TextField(blank=True)
    file = models.FileField(upload_to='chat_files/', null=True, blank=True)

    is_read = models.BooleanField(default=False)
    read_by = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='read_messages',
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.sender.username}: {self.content[:50]}"