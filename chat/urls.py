from django.urls import path
from .views import (
    ChatRoomListView,
    ChatRoomCreateView,
    ChatRoomDetailView,
    MessageListView,
    MessageCreateView,
    MarkMessagesReadView
)

urlpatterns = [
    # Chat Rooms
    path('rooms/', ChatRoomListView.as_view(), name='chatroom-list'),
    path('rooms/create/', ChatRoomCreateView.as_view(), name='chatroom-create'),
    path('rooms/<int:pk>/', ChatRoomDetailView.as_view(), name='chatroom-detail'),

    # Messages
    path('rooms/<int:room_id>/messages/', MessageListView.as_view(), name='message-list'),
    path('messages/send/', MessageCreateView.as_view(), name='message-create'),
    path('rooms/<int:room_id>/read/', MarkMessagesReadView.as_view(), name='mark-messages-read'),
]