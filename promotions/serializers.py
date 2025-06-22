from rest_framework import serializers
from .models import Promotion
from users.serializers import UserDetailSerializer

class PromotionSerializer(serializers.ModelSerializer):
    author = UserDetailSerializer(read_only=True)
    
    class Meta:
        model = Promotion
        fields = ['id', 'author', 'slogan', 'content', 'slug', 'status', 
                 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at', 'slug']

class PromotionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promotion
        fields = ['slogan', 'content', 'status']
    
    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data) 