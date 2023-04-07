from rest_framework import serializers
from User.models import Post

class PostSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    tags = serializers.ListField(source='tags.names')

    class Meta:
        model = Post
        fields = ['image', 'info', 'owner', 'tags', 'likes_count']