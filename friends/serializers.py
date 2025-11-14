from rest_framework import serializers
from .models import Friendship, Follow
from accounts.serializers import UserMinimalSerializer  # Changed from relative import

class FriendshipSerializer(serializers.ModelSerializer):
    """Serializer for Friendship model"""
    from_user = UserMinimalSerializer(read_only=True)
    to_user = UserMinimalSerializer(read_only=True)

    class Meta:
        model = Friendship
        fields = ['id', 'from_user', 'to_user', 'status', 'created_at', 'updated_at']
        read_only_fields = ['id', 'from_user', 'created_at', 'updated_at']


class FriendRequestSerializer(serializers.ModelSerializer):
    """Serializer for sending friend requests"""

    class Meta:
        model = Friendship
        fields = ['to_user']


class FollowSerializer(serializers.ModelSerializer):
    """Serializer for Follow model"""
    follower = UserMinimalSerializer(read_only=True)
    following = UserMinimalSerializer(read_only=True)

    class Meta:
        model = Follow
        fields = ['id', 'follower', 'following', 'created_at']
        read_only_fields = ['id', 'follower', 'created_at']