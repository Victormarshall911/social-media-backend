from django.urls import path
from .views import (
    PostListCreateView,
    PostDetailView,
    UserPostsView,
    LikePostView,
    CommentListCreateView,
    CommentDetailView,
    LikeCommentView
)

urlpatterns = [
    # Posts
    path('', PostListCreateView.as_view(), name='post-list-create'),
    path('<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('user/<int:user_id>/', UserPostsView.as_view(), name='user-posts'),

    # Likes
    path('<int:post_id>/like/', LikePostView.as_view(), name='like-post'),

    # Comments
    path('<int:post_id>/comments/', CommentListCreateView.as_view(), name='comment-list-create'),
    path('comments/<int:pk>/', CommentDetailView.as_view(), name='comment-detail'),
    path('comments/<int:comment_id>/like/', LikeCommentView.as_view(), name='like-comment'),
]