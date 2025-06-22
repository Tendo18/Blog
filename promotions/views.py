from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.response import Response
from .models import Promotion
from .serializers import PromotionSerializer, PromotionCreateSerializer

# Create your views here.

class PromotionListView(generics.ListAPIView):
    """GET /api/promotions - List all published promotions"""
    serializer_class = PromotionSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        return Promotion.objects.filter(status='published').select_related('author')

class PromotionCreateView(generics.CreateAPIView):
    """POST /api/promotions - Create new promotion"""
    serializer_class = PromotionCreateSerializer
    permission_classes = [IsAuthenticated]

class PromotionDetailView(generics.RetrieveAPIView):
    """GET /api/promotions/<slug> - Get promotion by slug"""
    serializer_class = PromotionSerializer
    permission_classes = [AllowAny]
    lookup_field = 'slug'
    
    def get_queryset(self):
        return Promotion.objects.filter(status='published').select_related('author')

class PromotionUpdateView(generics.UpdateAPIView):
    """PUT /api/promotions/<promotion_id> - Update promotion"""
    serializer_class = PromotionCreateSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Promotion.objects.filter(author=self.request.user)

class PromotionDeleteView(generics.DestroyAPIView):
    """DELETE /api/promotions/<promotion_id> - Delete promotion"""
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Promotion.objects.filter(author=self.request.user)
