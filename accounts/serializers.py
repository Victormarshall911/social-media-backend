from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model"""

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'bio', 'profile_picture', 'cover_photo', 'date_of_birth',
            'location', 'website', 'phone_number', 'followers_count',
            'following_count', 'posts_count', 'is_private', 'is_verified',
            'is_online', 'last_seen', 'created_at'
        ]
        read_only_fields = [
            'id', 'followers_count', 'following_count', 'posts_count',
            'is_verified', 'is_online', 'last_seen', 'created_at'
        ]


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for user registration"""
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2', 'first_name', 'last_name']

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating user profile"""

    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'bio', 'profile_picture',
            'cover_photo', 'date_of_birth', 'location', 'website',
            'phone_number', 'is_private'
        ]


class UserMinimalSerializer(serializers.ModelSerializer):
    """Minimal user info for nested serializers"""

    class Meta:
        model = User
        fields = ['id', 'username', 'profile_picture', 'is_verified']