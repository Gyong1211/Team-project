from rest_framework import serializers

from group.models import MyGroup
from group.serializers import GroupSerializer
from member.serializers import UserSerializer
from post.models import Post
from post.serializers.comment import CommentSerializer


class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    group = GroupSerializer(read_only=True)

    class Meta:
        model = Post
        fields = (
            'pk',
            'author',
            'group',
            'image',
            'video',
            'content',
            'comments',
            'like_users',
            'like_count'
        )
        read_only_fields = (
            'author',
            'group'
        )


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

    def validate(self, data):
        user = self.context['request'].user
        joined_group = MyGroup.objects.filter(member=user)
        if data['group'] not in joined_group:
            raise serializers.ValidationError('속한 그룹이 아닙니다.')
        return data


class PostUpdateSerializer(serializers.ModelSerializer):
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
            'group',
        )
