from django.urls import path
from . import views

urlpatterns = [
    # Blog Posts
    path('posts/published/', views.PublishedBlogPostListView.as_view(), name='published-posts'),
    path('posts/admin/', views.AdminBlogPostListView.as_view(), name='admin-posts'),
    path('posts/<slug:slug>/', views.BlogPostDetailView.as_view(), name='blog-post-detail'),
    path('posts/', views.BlogPostCreateView.as_view(), name='blog-post-create'),
    path('posts/<int:pk>/', views.BlogPostUpdateView.as_view(), name='blog-post-update'),
    path('posts/<int:pk>/delete/', views.BlogPostDeleteView.as_view(), name='blog-post-delete'),
    path('posts/<int:pk>/status/', views.BlogPostStatusUpdateView.as_view(), name='blog-post-status'),
    
    # Likes
    path('posts/<int:post_id>/like/', views.like_blog_post, name='like-post'),
    path('posts/<int:post_id>/unlike/', views.unlike_blog_post, name='unlike-post'),
    path('posts/<int:post_id>/like-count/', views.like_count, name='like-count'),
    
    # Bookmarks
    path('posts/<int:post_id>/bookmark/', views.bookmark_blog_post, name='bookmark-post'),
    path('posts/<int:post_id>/unbookmark/', views.unbookmark_blog_post, name='unbookmark-post'),
    path('posts/<int:post_id>/bookmark-count/', views.bookmark_count, name='bookmark-count'),
    
    # Comments
    path('posts/<int:post_id>/comments/', views.CommentListView.as_view(), name='comment-list'),
    path('comments/<int:pk>/delete/', views.CommentDeleteView.as_view(), name='comment-delete'),
    
    # Notifications
    path('notifications/', views.NotificationListView.as_view(), name='notification-list'),
    path('notifications/<int:notification_id>/read/', views.mark_notification_read, name='mark-notification-read'),
    path('notifications/read-all/', views.mark_all_notifications_read, name='mark-all-notifications-read'),
]