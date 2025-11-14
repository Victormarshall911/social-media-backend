from rest_framework import serializers
from .models import Post, Like, Comment, CommentLike
from accounts.serializers import UserMinimalSerializer  # Changed from relative import

class PostSerializer(serializers.ModelSerializer):
    """Serializer for Post model"""
    user = UserMinimalSerializer(read_only=True)
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'id', 'user', 'caption', 'image', 'video',
            'likes_count', 'comments_count', 'shares_count',
            'is_public', 'is_liked', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'likes_count', 'comments_count', 'shares_count', 'created_at', 'updated_at']

    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Like.objects.filter(user=request.user, post=obj).exists()
        return False


class PostCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating posts"""

    class Meta:
        model = Post
        fields = ['caption', 'image', 'video', 'is_public']


class LikeSerializer(serializers.ModelSerializer):
    """Serializer for Like model"""
    user = UserMinimalSerializer(read_only=True)

    class Meta:
        model = Like
        fields = ['id', 'user', 'post', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']


class CommentSerializer(serializers.ModelSerializer):
    """Serializer for Comment model"""
    user = UserMinimalSerializer(read_only=True)
    replies = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = [
            'id', 'user', 'post', 'text', 'parent',
            'likes_count', 'is_liked', 'replies',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'likes_count', 'created_at', 'updated_at']

    def get_replies(self, obj):
        if obj.replies.exists():
            return CommentSerializer(obj.replies.all(), many=True, context=self.context).data
        return []

    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return CommentLike.objects.filter(user=request.user, comment=obj).exists()
        return False