from django.contrib import admin
from .models import Promotion

@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    list_display = ('slogan', 'author', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('slogan', 'content', 'author__username')
    prepopulated_fields = {'slug': ('slogan',)}
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Content', {
            'fields': ('slogan', 'slug', 'content')
        }),
        ('Metadata', {
            'fields': ('author', 'status')
        }),
    )
