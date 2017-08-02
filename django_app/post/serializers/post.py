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

class PostUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = (
            'pk',
            'author',
            'content',
            'group',
            'image',
            'video',
        )
        read_only_fields = (
            'group',
        )

    # def update(self, instance, validated_data):
    #     raise_errors_on_nested_writes('update', self, validated_data)
    #     info = model_meta.get_field_info(instance)
    #
    #     # Simply set each attribute on the instance, and then save it.
    #     # Note that unlike `.create()` we don't need to treat many-to-many
    #     # relationships as being a special case. During updates we already
    #     # have an instance pk for the relationships to be associated with.
    #     for attr, value in validated_data.items():
    #         if attr in info.relations and info.relations[attr].to_many:
    #             set_many(instance, attr, value)
    #         else:
    #             setattr(instance, attr, value)
    #     instance.save()
    #
    #     return instance

    # Determine the fields to apply...