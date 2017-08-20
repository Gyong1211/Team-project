from rest_framework import serializers

from group.models import MyGroup
from group.serializers import GroupSerializer
from member.models import MyUser
from member.serializers import UserSerializer
from ..models import Post, PostLike
from .comment import CommentSerializer


class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    group = GroupSerializer(read_only=True)

    class Meta:
        model = Post
        fields = (
            'pk',
            'author',
            'group',
            'content',
            'image',
            'video',
            'like_count',
            'comment_count',
        )
        read_only_fields = (
            'pk',
            'author',
            'group',
            'like_count',
            'comment_count',
        )

    def to_representation(self, obj):
        ret = super().to_representation(obj)
        ret['is_like'] = self.context['request'].user in obj.like_users.all()
        return ret


class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = (
            'pk',
            'group',
            'content',
            'image',
            'video',
        )
        read_only_fields = (
            'created_date',
        )

    def validate(self, data):
        user = self.context['request'].user
        joined_group = user.group.all()
        if data['group'] not in joined_group:
            raise serializers.ValidationError('속한 그룹이 아닙니다.')
        return data


class PostUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = (
            'pk',
            'author',
            'group',
            'content',
            'image',
            'video',
            'like_count',
            'comment_count',
        )
        read_only_fields = (
            'pk',
            'author',
            'group',
            'like_count',
            'comment_count',
        )

    def to_representation(self, obj):
        ret = super().to_representation(obj)
        ret['is_like'] = self.context['request'].user in obj.like_users.all()
        return ret


class PostLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostLike
        field = (
            'pk',
            'user',
            'post',
        )
