from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    RegisterView,
    LoginView,
    LogoutView,
    UserProfileView,
    UserDetailView,
    UserSearchView
)

urlpatterns = [
    # Authentication
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # User Profile
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('users/search/', UserSearchView.as_view(), name='user-search'),
]