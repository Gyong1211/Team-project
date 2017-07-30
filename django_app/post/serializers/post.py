from rest_framework import serializers

from member.serializers import UserSerializer
from post.models import Post
from post.serializers import CommentSerializer


class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    comments = CommentSerializer(read_only=True)

    class Meta:
        model = Post
        fields = (
            'pk',
            'author',
            'group',
            'image',
            'content',
            'comments'
        )
        read_only_fields = (
            'author',
            'group'
        )