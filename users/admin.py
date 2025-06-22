from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Bookmark, Like

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_staff', 'is_active')
    list_filter = ('role', 'is_staff', 'is_active', 'created_at')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('-created_at',)
    
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('bio', 'photo', 'role')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Info', {'fields': ('bio', 'photo', 'role')}),
    )

@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display = ('user', 'blog_post_id', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username',)
    ordering = ('-created_at',)

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'blog_post_id', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username',)
    ordering = ('-created_at',)
