from rest_framework import serializers, request

from member.serializers import UserSerializer
from .tag import TagSerializer
from ..models import MyGroup


class GroupListSerializer(serializers.ModelSerializer):
    owner = UserSerializer(many=False, read_only=True)
    profile_img_url = serializers.SerializerMethodField(read_only=True)
    tags = TagSerializer(many=True, read_only=True, allow_null=True)
    tag = serializers.CharField(max_length=255, allow_blank=True, write_only=True)

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
            'tag',
        )
        read_only_fields = (
            'num_of_members',
        )

    def get_profile_img_url(self, obj):
        return obj.profile_img.url

    def create(self, validated_data):
        return MyGroup.objects.create(**validated_data, owner=self.context['request'].user)


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
