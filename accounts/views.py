from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model, authenticate
from .serializers import (
    UserSerializer,
    UserRegistrationSerializer,
    UserUpdateSerializer
)

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    """User registration endpoint"""
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = UserRegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)

        return Response({
            'user': UserSerializer(user).data,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            },
            'message': 'User registered successfully'
        }, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    """User login endpoint"""
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response(
                {'error': 'Please provide both email and password'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Authenticate user
        user = authenticate(username=email, password=password)

        if user is None:
            # Try with email field
            try:
                user_obj = User.objects.get(email=email)
                user = authenticate(username=user_obj.username, password=password)
            except User.DoesNotExist:
                pass

        if user is not None:
            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)

            # Update online status
            user.is_online = True
            user.save()

            return Response({
                'user': UserSerializer(user).data,
                'tokens': {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                },
                'message': 'Login successful'
            }, status=status.HTTP_200_OK)

        return Response(
            {'error': 'Invalid credentials'},
            status=status.HTTP_401_UNAUTHORIZED
        )


class LogoutView(APIView):
    """User logout endpoint"""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            # Update online status
            request.user.is_online = False
            request.user.save()

            # Blacklist the refresh token
            refresh_token = request.data.get("refresh")
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()

            return Response(
                {'message': 'Logout successful'},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class UserProfileView(generics.RetrieveUpdateAPIView):
    """Get and update user profile"""
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    def get_serializer_class(self):
        if self.request.method == 'PUT' or self.request.method == 'PATCH':
            return UserUpdateSerializer
        return UserSerializer


class UserDetailView(generics.RetrieveAPIView):
    """Get any user's profile by ID"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'pk'


class UserSearchView(generics.ListAPIView):
    """Search users by username or name"""
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        query = self.request.query_params.get('q', '')
        if query:
            return User.objects.filter(
                username__icontains=query
            ) | User.objects.filter(
                first_name__icontains=query
            ) | User.objects.filter(
                last_name__icontains=query
            )
        return User.objects.none()