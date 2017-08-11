from rest_framework import serializers

from member.serializers import UserSerializer
from ..models import Comment

__all__ = (
    'CommentSerializer',
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
