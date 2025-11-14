from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from django.db.models import Q
from .models import ChatRoom, Message
from .serializers import ChatRoomSerializer, MessageSerializer

User = get_user_model()


class ChatRoomListView(generics.ListAPIView):
    """List all chat rooms for the current user"""
    serializer_class = ChatRoomSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ChatRoom.objects.filter(
            participants=self.request.user
        ).order_by('-updated_at')


class ChatRoomCreateView(APIView):
    """Create a new chat room (direct or group)"""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        room_type = request.data.get('room_type', 'direct')
        participant_ids = request.data.get('participants', [])
        name = request.data.get('name', '')

        if not participant_ids:
            return Response(
                {'error': 'At least one participant is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # For direct messages, check if room already exists
        if room_type == 'direct' and len(participant_ids) == 1:
            other_user_id = participant_ids[0]
            existing_room = ChatRoom.objects.filter(
                room_type='direct',
                participants=request.user
            ).filter(
                participants__id=other_user_id
            ).first()

            if existing_room:
                return Response(
                    ChatRoomSerializer(existing_room, context={'request': request}).data,
                    status=status.HTTP_200_OK
                )

        # Create new room
        chat_room = ChatRoom.objects.create(
            room_type=room_type,
            name=name,
            created_by=request.user
        )

        # Add participants
        chat_room.participants.add(request.user)
        for user_id in participant_ids:
            try:
                user = User.objects.get(id=user_id)
                chat_room.participants.add(user)
            except User.DoesNotExist:
                pass

        return Response(
            ChatRoomSerializer(chat_room, context={'request': request}).data,
            status=status.HTTP_201_CREATED
        )


class ChatRoomDetailView(generics.RetrieveAPIView):
    """Get details of a specific chat room"""
    serializer_class = ChatRoomSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ChatRoom.objects.filter(participants=self.request.user)


class MessageListView(generics.ListAPIView):
    """List all messages in a chat room"""
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        room_id = self.kwargs.get('room_id')

        # Verify user is participant
        try:
            room = ChatRoom.objects.get(id=room_id, participants=self.request.user)
        except ChatRoom.DoesNotExist:
            return Message.objects.none()

        return Message.objects.filter(room_id=room_id).order_by('created_at')


class MessageCreateView(generics.CreateAPIView):
    """Send a message in a chat room"""
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        room_id = self.request.data.get('room')

        # Verify user is participant
        try:
            room = ChatRoom.objects.get(id=room_id, participants=self.request.user)
        except ChatRoom.DoesNotExist:
            return Response(
                {'error': 'Chat room not found or access denied'},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer.save(sender=self.request.user)

        # Update room's updated_at
        room.save()


class MarkMessagesReadView(APIView):
    """Mark messages as read"""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, room_id):
        try:
            room = ChatRoom.objects.get(id=room_id, participants=request.user)
        except ChatRoom.DoesNotExist:
            return Response(
                {'error': 'Chat room not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        # Mark all unread messages as read
        messages = Message.objects.filter(
            room=room
        ).exclude(sender=request.user).exclude(read_by=request.user)

        for message in messages:
            message.read_by.add(request.user)
            message.is_read = True
            message.save()

        return Response(
            {'message': f'{messages.count()} messages marked as read'},
            status=status.HTTP_200_OK
        )