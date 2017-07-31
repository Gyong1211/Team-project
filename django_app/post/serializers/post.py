from rest_framework import serializers

from member.serializers import UserSerializer
from post.models import Post
from post.serializers.comment import CommentSerializer


class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    post_img_url = serializers.SerializerMethodField(read_only=True)
    # post_video_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Post
        fields = (
            'pk',
            'author',
            'group',
            'post_img_url',
            # 'post_video_url',
            'content',
            'comments',
            'like_users',
            'like_count'
        )
        read_only_fields = (
            'author',
            'group'
        )

    def get_post_img_url(self, obj):
        if obj.image:
            return obj.image.url
        else:
            return None

    # def get_post_video_url(self, obj):
    #     return obj.video.url


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

    def create(self, validated_data):
        return Post.objects.create(**validated_data, author=self.context['request'].user)
