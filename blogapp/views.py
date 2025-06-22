from django.shortcuts import render, get_object_or_404
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.utils import timezone
from users.models import Like, Bookmark

from .models import BlogPost, Comment, Notification
from .serializers import (
    BlogPostSerializer, BlogPostCreateSerializer, BlogPostUpdateSerializer,
    CommentSerializer, NotificationSerializer
)

# Blog Post Views
class PublishedBlogPostListView(generics.ListAPIView):
    """GET /api/posts/published - List all published blog posts"""
    serializer_class = BlogPostSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        return BlogPost.objects.filter(status='published').select_related('author')

class AdminBlogPostListView(generics.ListAPIView):
    """GET /api/posts/admin - Admin-only view of all blog posts"""
    serializer_class = BlogPostSerializer
    permission_classes = [IsAdminUser]
    
    def get_queryset(self):
        return BlogPost.objects.all().select_related('author')

class BlogPostDetailView(generics.RetrieveAPIView):
    """GET /api/posts/<slug> - Get blog post by slug"""
    serializer_class = BlogPostSerializer
    permission_classes = [AllowAny]
    lookup_field = 'slug'
    
    def get_queryset(self):
        return BlogPost.objects.filter(status='published').select_related('author')

class BlogPostCreateView(generics.CreateAPIView):
    """POST /api/posts - Create new blog post"""
    serializer_class = BlogPostCreateSerializer
    permission_classes = [IsAuthenticated]

class BlogPostUpdateView(generics.UpdateAPIView):
    """PUT /api/posts/<post_id> - Update blog post"""
    serializer_class = BlogPostUpdateSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return BlogPost.objects.filter(author=self.request.user)

class BlogPostDeleteView(generics.DestroyAPIView):
    """DELETE /api/posts/<post_id> - Delete blog post"""
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return BlogPost.objects.filter(author=self.request.user)

class BlogPostStatusUpdateView(generics.UpdateAPIView):
    """PUT /api/posts/<post_id>/status - Update blog post status (admin only)"""
    serializer_class = BlogPostUpdateSerializer
    permission_classes = [IsAdminUser]
    
    def get_queryset(self):
        return BlogPost.objects.all()
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        status = request.data.get('status')
        if status == 'published' and not instance.published_at:
            instance.published_at = timezone.now()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({
            'message': 'Blog post status updated successfully',
            'blog_post': BlogPostSerializer(instance).data
        })

# Like Views
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def like_blog_post(request, post_id):
    """POST /api/posts/<post_id>/like - Like a blog post"""
    blog_post = get_object_or_404(BlogPost, id=post_id)
    user = request.user
    
    like, created = Like.objects.get_or_create(user=user, blog_post=blog_post)
    
    if created:
        # Create notification
        Notification.objects.create(
            recipient=blog_post.author,
            sender=user,
            notification_type='like',
            blog_post=blog_post,
            message=f'{user.username} liked your post "{blog_post.title}"'
        )
        return Response({'message': 'Post liked successfully'}, status=status.HTTP_201_CREATED)
    else:
        return Response({'message': 'Post already liked'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def unlike_blog_post(request, post_id):
    """DELETE /api/posts/<post_id>/like - Unlike a blog post"""
    blog_post = get_object_or_404(BlogPost, id=post_id)
    user = request.user
    
    try:
        like = Like.objects.get(user=user, blog_post=blog_post)
        like.delete()
        return Response({'message': 'Post unliked successfully'}, status=status.HTTP_200_OK)
    except Like.DoesNotExist:
        return Response({'message': 'Post not liked'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([AllowAny])
def like_count(request, post_id):
    """GET /api/posts/<post_id>/like-count - Get like count for a blog post"""
    blog_post = get_object_or_404(BlogPost, id=post_id)
    return Response({'like_count': blog_post.like_count})

# Bookmark Views
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def bookmark_blog_post(request, post_id):
    """POST /api/posts/<post_id>/bookmark - Bookmark a blog post"""
    blog_post = get_object_or_404(BlogPost, id=post_id)
    user = request.user
    
    bookmark, created = Bookmark.objects.get_or_create(user=user, blog_post=blog_post)
    
    if created:
        return Response({'message': 'Post bookmarked successfully'}, status=status.HTTP_201_CREATED)
    else:
        return Response({'message': 'Post already bookmarked'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def unbookmark_blog_post(request, post_id):
    """DELETE /api/posts/<post_id>/bookmark - Remove bookmark from a blog post"""
    blog_post = get_object_or_404(BlogPost, id=post_id)
    user = request.user
    
    try:
        bookmark = Bookmark.objects.get(user=user, blog_post=blog_post)
        bookmark.delete()
        return Response({'message': 'Bookmark removed successfully'}, status=status.HTTP_200_OK)
    except Bookmark.DoesNotExist:
        return Response({'message': 'Post not bookmarked'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([AllowAny])
def bookmark_count(request, post_id):
    """GET /api/posts/<post_id>/bookmark-count - Get bookmark count for a blog post"""
    blog_post = get_object_or_404(BlogPost, id=post_id)
    return Response({'bookmark_count': blog_post.bookmark_count})

# Comment Views
class CommentListView(generics.ListCreateAPIView):
    """GET/POST /api/posts/<post_id>/comments - List and create comments for a blog post"""
    serializer_class = CommentSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        post_id = self.kwargs['post_id']
        return Comment.objects.filter(blog_post_id=post_id, parent=None, is_approved=True)
    
    def perform_create(self, serializer):
        post_id = self.kwargs['post_id']
        blog_post = get_object_or_404(BlogPost, id=post_id)
        serializer.save(author=self.request.user, blog_post=blog_post)
        
        # Create notification for blog post author
        if self.request.user != blog_post.author:
            Notification.objects.create(
                recipient=blog_post.author,
                sender=self.request.user,
                notification_type='comment',
                blog_post=blog_post,
                message=f'{self.request.user.username} commented on your post "{blog_post.title}"'
            )

class CommentDeleteView(generics.DestroyAPIView):
    """DELETE /api/comments/<comment_id> - Delete a comment"""
    queryset = Comment.objects.all()
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Comment.objects.filter(author=self.request.user)

# Notification Views
class NotificationListView(generics.ListAPIView):
    """GET /api/notifications - List user notifications"""
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Notification.objects.filter(recipient=self.request.user)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mark_notification_read(request, notification_id):
    """POST /api/notifications/<notification_id>/read - Mark notification as read"""
    notification = get_object_or_404(Notification, id=notification_id, recipient=request.user)
    notification.is_read = True
    notification.save()
    return Response({'message': 'Notification marked as read'})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mark_all_notifications_read(request):
    """POST /api/notifications/read-all - Mark all notifications as read"""
    Notification.objects.filter(recipient=request.user, is_read=False).update(is_read=True)
    return Response({'message': 'All notifications marked as read'})


