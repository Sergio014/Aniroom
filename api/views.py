from rest_framework import generics
from . import serializers
from User.models import Post


class PostsListView(generics.ListAPIView):
    serializer_class = serializers.PostSerializer
    queryset = Post.objects.all()
    
    def get_queryset(self):
        return super().get_queryset()