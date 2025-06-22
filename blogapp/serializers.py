from rest_framework import serializers
from .models import BlogPost, Comment, Notification
from users.serializers import UserDetailSerializer

class CommentSerializer(serializers.ModelSerializer):
    author = UserDetailSerializer(read_only=True)
    replies = serializers.SerializerMethodField()
    replies_count = serializers.ReadOnlyField()
    
    class Meta:
        model = Comment
        fields = ['id', 'author', 'content', 'parent', 'replies', 'replies_count', 
                 'created_at', 'updated_at', 'is_approved']
        read_only_fields = ['created_at', 'updated_at', 'is_approved']
    
    def get_replies(self, obj):
        if obj.replies.exists():
            return CommentSerializer(obj.replies.all(), many=True).data
        return []

class BlogPostSerializer(serializers.ModelSerializer):
    author = UserDetailSerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    like_count = serializers.ReadOnlyField()
    bookmark_count = serializers.ReadOnlyField()
    comment_count = serializers.ReadOnlyField()
    is_liked = serializers.SerializerMethodField()
    is_bookmarked = serializers.SerializerMethodField()
    
    class Meta:
        model = BlogPost
        fields = ['id', 'author', 'title', 'slug', 'content', 'excerpt', 'status',
                 'read_time', 'featured_image', 'created_at', 'updated_at', 
                 'published_at', 'comments', 'like_count', 'bookmark_count', 
                 'comment_count', 'is_liked', 'is_bookmarked']
        read_only_fields = ['created_at', 'updated_at', 'published_at', 'slug']
    
    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.likes.filter(user=request.user).exists()
        return False
    
    def get_is_bookmarked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.bookmarked_by.filter(user=request.user).exists()
        return False

class BlogPostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPost
        fields = ['title', 'content', 'excerpt', 'status', 'read_time', 'featured_image']
    
    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)

class BlogPostUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPost
        fields = ['title', 'content', 'excerpt', 'status', 'read_time', 'featured_image']

class NotificationSerializer(serializers.ModelSerializer):
    sender = UserDetailSerializer(read_only=True)
    blog_post_title = serializers.ReadOnlyField(source='blog_post.title')
    
    class Meta:
        model = Notification
        fields = ['id', 'sender', 'notification_type', 'blog_post_title', 
                 'message', 'is_read', 'created_at']
        read_only_fields = ['created_at']

           

       
