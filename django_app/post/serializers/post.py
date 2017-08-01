from rest_framework import serializers

from member.serializers import UserSerializer
from post.models import Post
from post.serializers.comment import CommentSerializer


class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    # post_img_url = serializers.SerializerMethodField(read_only=True)

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
            # 'group'
        )

    # def get_post_img_url(self, obj):
    #     if obj.image:
    #         return obj.image.url
    #     else:
    #         return None



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

# class PostUpdateSerializer(serializers.ModelSerializer):
