from django.shortcuts import render
from .models import User, Bookmark, Like
from rest_framework import generics, status
from .serializers import UserSerializer, UserDetailSerializer, CustomTokenObtainPairSerializer, BookmarkSerializer, LikeSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework.exceptions import ValidationError
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_object_or_404

#Views for registration 
class RegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "message": "User registered successfully", 
            "user": UserDetailSerializer(user).data
        }, status=status.HTTP_201_CREATED)
    
#Views for login and token generation
class LoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        required_fields = {'email', 'password'}
        if not required_fields.issubset(request.data):
            return Response(
                {"error": "Email and password are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception:
            return Response(
                {"error": "Invalid email or password."},
                status=status.HTTP_401_UNAUTHORIZED
            )

        return Response({
            "access": serializer.validated_data['access'],
            "refresh": serializer.validated_data['refresh'],
            "user": serializer.validated_data['user'],
            "message": "Login successful"
        }, status=status.HTTP_200_OK)

#Views for user profile
class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        return self.request.user
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = UserDetailSerializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({
            "message": "Profile updated successfully", 
            "user": UserDetailSerializer(instance).data
        }, status=status.HTTP_200_OK)

#Views for user details by ID
class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

#Views for bookmarks
class BookmarkListView(generics.ListAPIView):
    serializer_class = BookmarkSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Bookmark.objects.filter(user=self.request.user)

class BookmarkCreateView(generics.CreateAPIView):
    serializer_class = BookmarkSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class BookmarkDeleteView(generics.DestroyAPIView):
    queryset = Bookmark.objects.all()
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        return get_object_or_404(Bookmark, user=self.request.user, blog_post_id=self.kwargs['post_id'])

#Views for likes
class LikeListView(generics.ListAPIView):
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Like.objects.filter(user=self.request.user)

class LikeCreateView(generics.CreateAPIView):
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class LikeDeleteView(generics.DestroyAPIView):
    queryset = Like.objects.all()
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        return get_object_or_404(Like, user=self.request.user, blog_post_id=self.kwargs['post_id'])

#Password reset view
@api_view(['POST'])
@permission_classes([AllowAny])
def forgot_password(request):
    email = request.data.get('email')
    if not email:
        return Response({'error': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        user = User.objects.get(email=email)
        # Here you would typically send a password reset email
        # For now, we'll just return a success message
        return Response({
            'message': 'Password reset email sent successfully'
        }, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({
            'error': 'User with this email does not exist'
        }, status=status.HTTP_404_NOT_FOUND)