from django.db import models
from django.conf import settings
from django.utils.text import slugify

class Promotion(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    )
    
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='promotions')
    slogan = models.CharField(max_length=200)
    content = models.TextField()
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.slogan
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.slogan)
        super().save(*args, **kwargs)
