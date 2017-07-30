from rest_framework import serializers, request

from member.serializers import UserSerializer
from .tag import TagSerializer
from ..models import MyGroup


class GroupListSerializer(serializers.ModelSerializer):
    owner = UserSerializer(many=False)
    profile_img_url = serializers.SerializerMethodField()
    tags = TagSerializer(many=True, read_only=True, allow_null=True)

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

    def get_profile_img_url(self, obj):
        return obj.profile_img.url


class GroupDetailSerializer(serializers.ModelSerializer):
    owner = UserSerializer(many=False)
    profile_img_url = serializers.SerializerMethodField()
    member = UserSerializer(many=True)
    tags = TagSerializer(many=True, read_only=True, allow_null=True)

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
            'member',
            'tags',
        )

    def get_profile_img_url(self, obj):
        return obj.profile_img.url
