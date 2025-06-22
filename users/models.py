from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from datetime import datetime, timedelta
from django.utils import timezone

# Create your models here.
#Define the User roles
class User(AbstractUser):
    ROLE_CHOICES = (
        ('user', 'User'),
        ('admin', 'Admin'),
    )       

    
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=50, unique=True)
    bio = models.TextField(blank=True)
    photo = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')
    liked_blogs = models.ManyToManyField('blogapp.BlogPost', blank=True, related_name='liked_by')
    created_at = models.DateTimeField(default=timezone.now)

class Bookmark(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookmarks')
    blog_post_id = models.IntegerField()  # Temporary field
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'blog_post_id']
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} bookmarked post {self.blog_post_id}"

class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='likes')
    blog_post_id = models.IntegerField()  # Temporary field
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'blog_post_id']
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} liked post {self.blog_post_id}"

