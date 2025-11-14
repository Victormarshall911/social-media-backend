from django.urls import path
from .views import (
    SendFriendRequestView,
    FriendRequestListView,
    AcceptFriendRequestView,
    RejectFriendRequestView,
    FriendsListView,
    FollowUserView,
    FollowersListView,
    FollowingListView
)

urlpatterns = [
    # Friend Requests
    path('request/', SendFriendRequestView.as_view(), name='send-friend-request'),
    path('requests/', FriendRequestListView.as_view(), name='friend-request-list'),
    path('requests/<int:friendship_id>/accept/', AcceptFriendRequestView.as_view(), name='accept-friend-request'),
    path('requests/<int:friendship_id>/reject/', RejectFriendRequestView.as_view(), name='reject-friend-request'),
    path('list/', FriendsListView.as_view(), name='friends-list'),

    # Follow System
    path('follow/<int:user_id>/', FollowUserView.as_view(), name='follow-user'),
    path('followers/<int:user_id>/', FollowersListView.as_view(), name='followers-list'),
    path('following/<int:user_id>/', FollowingListView.as_view(), name='following-list'),
]