from django.shortcuts import render
from rest_framework import generics, permissions

from .models import Post
from .serializers import PostSerializer
from .permissions import IsAuthorReadOnly

# Create your views here.
class PostList (generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthorReadOnly,)   
    queryset = Post.objects.all()
    serializer_class = PostSerializer


