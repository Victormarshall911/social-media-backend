from django.db import models
from django.conf import settings


class Post(models.Model):
    """Post model for user posts"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='posts'
    )
    caption = models.TextField(max_length=2200, blank=True)
    image = models.ImageField(upload_to='posts/', null=True, blank=True)
    video = models.FileField(upload_to='videos/', null=True, blank=True)

    # Engagement metrics
    likes_count = models.IntegerField(default=0)
    comments_count = models.IntegerField(default=0)
    shares_count = models.IntegerField(default=0)

    # Privacy
    is_public = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'

    def __str__(self):
        return f"Post by {self.user.username} - {self.created_at.strftime('%Y-%m-%d')}"


class Like(models.Model):
    """Like model for posts"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='likes'
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='post_likes'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')  # User can only like a post once
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} likes {self.post.id}"


class Comment(models.Model):
    """Comment model for posts"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='post_comments'
    )
    text = models.TextField(max_length=500)
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='replies'
    )  # For nested comments/replies

    likes_count = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Comment by {self.user.username} on post {self.post.id}"


class CommentLike(models.Model):
    """Like model for comments"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    comment = models.ForeignKey(
        Comment,
        on_delete=models.CASCADE,
        related_name='comment_likes'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'comment')

    def __str__(self):
        return f"{self.user.username} likes comment {self.comment.id}"