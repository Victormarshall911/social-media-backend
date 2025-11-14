from django.db import models
from django.conf import settings


class Friendship(models.Model):
    """Model for friend relationships"""
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('blocked', 'Blocked'),
    )

    from_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='friendships_sent'
    )
    to_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='friendships_received'
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='pending'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('from_user', 'to_user')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.from_user.username} -> {self.to_user.username} ({self.status})"

    def accept(self):
        """Accept friend request"""
        self.status = 'accepted'
        self.save()

        # Update followers/following count
        self.from_user.following_count += 1
        self.to_user.followers_count += 1
        self.from_user.save()
        self.to_user.save()

    def reject(self):
        """Reject friend request"""
        self.status = 'rejected'
        self.save()


class Follow(models.Model):
    """Model for following users (one-way relationship)"""
    follower = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='following'
    )
    following = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='followers'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'following')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.follower.username} follows {self.following.username}"