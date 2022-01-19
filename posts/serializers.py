from rest_framework import serializers
from .models import Post, PostLike


class PostSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())
    likes = serializers.ReadOnlyField()

    class Meta:
        model = Post
        fields = ('id', 'title', 'body', 'author', 'likes')


class LikeSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = PostLike
        fields = ('user', 'post', 'liked_at')
