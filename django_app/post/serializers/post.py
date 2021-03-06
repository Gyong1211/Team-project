from rest_framework import serializers

from group.serializers import GroupSerializer
from member.serializers import UserSerializer
from ..models import Post, PostLike


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
            'created_date'
        )
        read_only_fields = (
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
            'created_date'
        )
        read_only_fields = (
            'author',
            'group',
            'like_count',
            'comment_count',
            'created_date'
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
            'created_date'
        )
