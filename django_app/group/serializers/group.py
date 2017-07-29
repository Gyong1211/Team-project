from rest_framework import serializers, request

from member.serializers import UserSerializer
from .tag import TagSerializer
from ..models import MyGroup


class GroupSerializer(serializers.ModelSerializer):
    owner = UserSerializer(many=False)
    members = UserSerializer(many=True)
    tags = TagSerializer(many=True, read_only=True, allow_null=True)

    class Meta:
        model = MyGroup
        fields = (
            'pk',
            'name',
            'owner',
            'group_type',
            'profile_img',
            'description',
            'members',
            'tags',
        )

