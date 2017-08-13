from rest_framework import serializers

from member.serializers import UserSerializer
from ..models import Comment

__all__ = (
    'CommentSerializer',
    'CommentUpdateSerializer',
)


class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = (
            'pk',
            'post',
            'author',
            'content',
            'created_date'
        )
        read_only_fields = (
            'created_date',
        )


class CommentUpdateSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    content = serializers.CharField(required=True)

    class Meta:
        model = Comment
        fields = (
            'pk',
            'post',
            'author',
            'content',
            'created_date'
        )
        read_only_fields = (
            'post',
            'created_date',
        )
