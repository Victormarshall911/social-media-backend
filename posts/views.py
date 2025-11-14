from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q
from .models import Post, Like, Comment, CommentLike
from .serializers import (
    PostSerializer,
    PostCreateSerializer,
    LikeSerializer,
    CommentSerializer
)


class PostListCreateView(generics.ListCreateAPIView):
    """List all posts (feed) and create new post"""
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return PostCreateSerializer
        return PostSerializer

    def get_queryset(self):
        # Get posts from user and their friends
        user = self.request.user
        return Post.objects.filter(
            Q(user=user) | Q(is_public=True)
        ).select_related('user').order_by('-created_at')

    def perform_create(self, serializer):
        post = serializer.save(user=self.request.user)
        # Update user's post count
        self.request.user.posts_count += 1
        self.request.user.save()


class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Get, update, or delete a specific post"""
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return PostCreateSerializer
        return PostSerializer

    def perform_destroy(self, instance):
        # Update user's post count
        instance.user.posts_count -= 1
        instance.user.save()
        instance.delete()


class UserPostsView(generics.ListAPIView):
    """Get all posts by a specific user"""
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        return Post.objects.filter(user_id=user_id).order_by('-created_at')


class LikePostView(APIView):
    """Like or unlike a post"""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response(
                {'error': 'Post not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        # Check if already liked
        like, created = Like.objects.get_or_create(
            user=request.user,
            post=post
        )

        if not created:
            # Unlike
            like.delete()
            post.likes_count -= 1
            post.save()
            return Response(
                {'message': 'Post unliked', 'liked': False},
                status=status.HTTP_200_OK
            )
        else:
            # Like
            post.likes_count += 1
            post.save()
            return Response(
                {'message': 'Post liked', 'liked': True},
                status=status.HTTP_201_CREATED
            )


class CommentListCreateView(generics.ListCreateAPIView):
    """List and create comments on a post"""
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        post_id = self.kwargs.get('post_id')
        # Only get top-level comments (no parent)
        return Comment.objects.filter(
            post_id=post_id,
            parent__isnull=True
        ).order_by('-created_at')

    def perform_create(self, serializer):
        post_id = self.kwargs.get('post_id')
        post = Post.objects.get(id=post_id)
        comment = serializer.save(user=self.request.user, post=post)

        # Update post's comment count
        post.comments_count += 1
        post.save()


class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Get, update, or delete a comment"""
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_destroy(self, instance):
        # Update post's comment count
        instance.post.comments_count -= 1
        instance.post.save()
        instance.delete()


class LikeCommentView(APIView):
    """Like or unlike a comment"""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, comment_id):
        try:
            comment = Comment.objects.get(id=comment_id)
        except Comment.DoesNotExist:
            return Response(
                {'error': 'Comment not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        like, created = CommentLike.objects.get_or_create(
            user=request.user,
            comment=comment
        )

        if not created:
            like.delete()
            comment.likes_count -= 1
            comment.save()
            return Response(
                {'message': 'Comment unliked', 'liked': False},
                status=status.HTTP_200_OK
            )
        else:
            comment.likes_count += 1
            comment.save()
            return Response(
                {'message': 'Comment liked', 'liked': True},
                status=status.HTTP_201_CREATED
            )