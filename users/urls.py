from django.urls import path
from . import views

urlpatterns = [
    # Authentication
    path('auth/register/', views.RegistrationView.as_view(), name='register'),
    path('auth/login/', views.LoginView.as_view(), name='login'),
    path('users/forgot-password/', views.forgot_password, name='forgot-password'),
    
    # User management
    path('users/<int:id>/', views.UserDetailView.as_view(), name='user-detail'),
    path('users/update/', views.ProfileView.as_view(), name='profile-update'),
    
    # Bookmarks
    path('bookmarks/', views.BookmarkListView.as_view(), name='bookmark-list'),
    path('bookmarks/create/', views.BookmarkCreateView.as_view(), name='bookmark-create'),
    path('bookmarks/<int:post_id>/delete/', views.BookmarkDeleteView.as_view(), name='bookmark-delete'),
    
    # Likes
    path('likes/', views.LikeListView.as_view(), name='like-list'),
    path('likes/create/', views.LikeCreateView.as_view(), name='like-create'),
    path('likes/<int:post_id>/delete/', views.LikeDeleteView.as_view(), name='like-delete'),
]