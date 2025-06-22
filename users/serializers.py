from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from datetime import datetime, timedelta    
from .models import User, Bookmark, Like
User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'first_name', 'last_name',
                   'bio', 'photo', 'role', 'created_at']
        extra_kwargs = {
            'password': {'write_only': True},
            'role': {'read_only': True},
            'email': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
            'created_at': {'read_only': True},
        }

    def create(self, validated_data):
       user = User.objects.create_user(**validated_data)
       return user
    
    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        if password:
            instance.set_password(password)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

class UserDetailSerializer(serializers.ModelSerializer):
    """Simplified serializer for user details in token responses"""
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'bio', 'photo', 'role']

class BookmarkSerializer(serializers.ModelSerializer):
    blog_post_title = serializers.ReadOnlyField(source='blog_post.title')
    blog_post_slug = serializers.ReadOnlyField(source='blog_post.slug')
    
    class Meta:
        model = Bookmark
        fields = ['id', 'blog_post', 'blog_post_title', 'blog_post_slug', 'created_at']
        read_only_fields = ['created_at']

class LikeSerializer(serializers.ModelSerializer):
    blog_post_title = serializers.ReadOnlyField(source='blog_post.title')
    blog_post_slug = serializers.ReadOnlyField(source='blog_post.slug')
    
    class Meta:
        model = Like
        fields = ['id', 'blog_post', 'blog_post_title', 'blog_post_slug', 'created_at']
        read_only_fields = ['created_at']

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    #override default field to use email instead of username
    #means users can login with email instead of username
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #remove the default username field
        self.fields.pop('username', None)
        #add email field
        self.fields['email'] = serializers.EmailField(required=True)
        self.fields['password'] = serializers.CharField(write_only=True, required=True)

    @classmethod
    def get_token(cls, user):
        return super().get_token(user)
    
    def validate(self, attrs):
        #extract email and password from request
        email = attrs.get('email')
        password = attrs.get('password')

        if not email or not password:   
            raise serializers.ValidationError("Email and password are required")
        
        #check for email and password
        user = User.objects.filter(email=email).first()
        if user and user.check_password(password):
            self.user = user
        else:
            raise serializers.ValidationError("Invalid email or password")
        
        #Generate token
        data = {}
        refresh_token = self.get_token(user)
        data['refresh'] = str(refresh_token)
        data['access'] = str(refresh_token.access_token)
        data['user'] = UserDetailSerializer(user).data
        return data    
