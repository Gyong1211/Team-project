from rest_framework import serializers, request

from member.serializers import UserSerializer
from .tag import TagSerializer
from ..models import MyGroup, GroupTag


class GroupSerializer(serializers.ModelSerializer):
    owner = UserSerializer(many=False, read_only=True)
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = MyGroup
        fields = (
            'pk',
            'name',
            'profile_img',
            'owner',
            'group_type',
            'description',
            'num_of_members',
            'tags',
        )
        read_only_fields = (
            'num_of_members',
        )


class GroupCreateSerializer(serializers.ModelSerializer):
    tag = serializers.CharField(max_length=255, write_only=True, allow_blank=True)
    owner = UserSerializer(read_only=True)

    class Meta:
        model = MyGroup
        fields = (
            'pk',
            'owner',
            'name',
            'profile_img',
            'group_type',
            'description',
            'tag'
        )
        read_only_fields = (
            'owner',
        )


class GroupUpdateSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True,read_only=True)
    tag_names = serializers.ListField(
        child=serializers.CharField(),
        required=False,
        write_only=True
    )

    class Meta:
        model = MyGroup
        fields = (
            'pk',
            'name',
            'profile_img',
            'group_type',
            'description',
            'tags',
            'tag_names',
        )

    def update(self, instance, validated_data):
        tag_name_list = validated_data.get('tag_names')
        updated_instance = super().update(instance, validated_data)
        if tag_name_list and isinstance(tag_name_list, list):
            updated_instance.tags.clear()
            for tag_name in tag_name_list:
                tag, created = GroupTag.objects.get_or_create(name=tag_name)
                updated_instance.add_tag(tag)
        return updated_instance
