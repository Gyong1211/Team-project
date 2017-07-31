from rest_framework import serializers, request

from member.serializers import UserSerializer
from .tag import TagSerializer
from ..models import MyGroup


class GroupSerializer(serializers.ModelSerializer):
    owner = UserSerializer(many=False, read_only=True)
    profile_img_url = serializers.SerializerMethodField(read_only=True)
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = MyGroup
        fields = (
            'pk',
            'name',
            'profile_img_url',
            'owner',
            'group_type',
            'description',
            'num_of_members',
            'tags',
        )
        read_only_fields = (
            'num_of_members',
        )

    def get_profile_img_url(self, obj):
        return obj.profile_img.url


class GroupCreateSerializer(serializers.ModelSerializer):
    tag = serializers.CharField(max_length=255, write_only=True, allow_blank=True)

    class Meta:
        model = MyGroup
        fields = (
            'pk',
            'name',
            'profile_img',
            'group_type',
            'description',
            'tag'
        )

    def create(self, validated_data):
        return MyGroup.objects.create(**validated_data, owner=self.context['request'].user)


class GroupUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyGroup
        fields = (
            'pk',
            'name',
            'profile_img',
            'group_type',
            'description',
            'tags'
        )
