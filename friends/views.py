from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from django.db.models import Q  # Add this import
from .models import Friendship, Follow
from .serializers import FriendshipSerializer, FollowSerializer, FriendRequestSerializer

User = get_user_model()


class SendFriendRequestView(APIView):
    """Send a friend request"""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        to_user_id = request.data.get('to_user')

        if not to_user_id:
            return Response(
                {'error': 'to_user is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            to_user = User.objects.get(id=to_user_id)
        except User.DoesNotExist:
            return Response(
                {'error': 'User not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        if to_user == request.user:
            return Response(
                {'error': 'Cannot send friend request to yourself'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check if friendship already exists
        existing = Friendship.objects.filter(
            from_user=request.user,
            to_user=to_user
        ).first()

        if existing:
            return Response(
                {'error': f'Friend request already {existing.status}'},
                status=status.HTTP_400_BAD_REQUEST
            )

        friendship = Friendship.objects.create(
            from_user=request.user,
            to_user=to_user,
            status='pending'
        )

        return Response(
            FriendshipSerializer(friendship).data,
            status=status.HTTP_201_CREATED
        )


class FriendRequestListView(generics.ListAPIView):
    """List all pending friend requests received"""
    serializer_class = FriendshipSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Friendship.objects.filter(
            to_user=self.request.user,
            status='pending'
        )


class AcceptFriendRequestView(APIView):
    """Accept a friend request"""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, friendship_id):
        try:
            friendship = Friendship.objects.get(
                id=friendship_id,
                to_user=request.user,
                status='pending'
            )
        except Friendship.DoesNotExist:
            return Response(
                {'error': 'Friend request not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        friendship.accept()

        return Response(
            {'message': 'Friend request accepted'},
            status=status.HTTP_200_OK
        )


class RejectFriendRequestView(APIView):
    """Reject a friend request"""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, friendship_id):
        try:
            friendship = Friendship.objects.get(
                id=friendship_id,
                to_user=request.user,
                status='pending'
            )
        except Friendship.DoesNotExist:
            return Response(
                {'error': 'Friend request not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        friendship.reject()

        return Response(
            {'message': 'Friend request rejected'},
            status=status.HTTP_200_OK
        )


class FriendsListView(generics.ListAPIView):
    """List all friends"""
    serializer_class = FriendshipSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Friendship.objects.filter(
            status='accepted'
        ).filter(
            Q(from_user=user) | Q(to_user=user)
        )


class FollowUserView(APIView):
    """Follow or unfollow a user"""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        try:
            user_to_follow = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response(
                {'error': 'User not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        if user_to_follow == request.user:
            return Response(
                {'error': 'Cannot follow yourself'},
                status=status.HTTP_400_BAD_REQUEST
            )

        follow, created = Follow.objects.get_or_create(
            follower=request.user,
            following=user_to_follow
        )

        if not created:
            # Unfollow
            follow.delete()
            return Response(
                {'message': 'Unfollowed', 'following': False},
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {'message': 'Following', 'following': True},
                status=status.HTTP_201_CREATED
            )


class FollowersListView(generics.ListAPIView):
    """List user's followers"""
    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user_id = self.kwargs.get('user_id', self.request.user.id)
        return Follow.objects.filter(following_id=user_id)


class FollowingListView(generics.ListAPIView):
    """List users that user is following"""
    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user_id = self.kwargs.get('user_id', self.request.user.id)
        return Follow.objects.filter(follower_id=user_id)