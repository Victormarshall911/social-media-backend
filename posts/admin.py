from django.contrib import admin
from .models import Post, Like, Comment, CommentLike


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'caption_preview', 'likes_count', 'comments_count', 'is_public', 'created_at']
    list_filter = ['is_public', 'created_at']
    search_fields = ['user__username', 'caption']
    readonly_fields = ['likes_count', 'comments_count', 'created_at', 'updated_at']
    ordering = ['-created_at']

    def caption_preview(self, obj):
        return obj.caption[:50] + '...' if len(obj.caption) > 50 else obj.caption

    caption_preview.short_description = 'Caption'


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'post', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'post__id']
    ordering = ['-created_at']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'post', 'text_preview', 'parent', 'likes_count', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'text', 'post__id']
    readonly_fields = ['likes_count', 'created_at', 'updated_at']
    ordering = ['-created_at']

    def text_preview(self, obj):
        return obj.text[:50] + '...' if len(obj.text) > 50 else obj.text

    text_preview.short_description = 'Comment'


@admin.register(CommentLike)
class CommentLikeAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'comment', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username']
    ordering = ['-created_at']