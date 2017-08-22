from rest_framework import serializers, request

from member.models import MyUser
from member.serializers import UserSerializer
from .tag import TagSerializer
from ..models import MyGroup, GroupTag

__all__ = (
    'GroupSerializer',
    'GroupCreateSerializer',
    'GroupUpdateSerializer',
    'GroupOwnerUpdateSerializer',
)


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

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        user = self.context['request'].user
        if user.is_authenticated:
            ret['is_member'] = user.membership_set.filter(group=instance).exists()
            if ret['is_member']:
                ret['is_owner'] = instance.owner == user
        return ret


class GroupCreateSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    tag_names = serializers.ListField(
        child=serializers.CharField(),
        required=False,
        write_only=True
    )
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
            'tags',
            'tag_names'
        )
        read_only_fields = (
            'owner',
        )

    def create(self, validated_data):
        tag_name_list = validated_data.pop('tag_names', '')
        group = MyGroup.objects.create(**validated_data)
        for tag_name in tag_name_list:
            tag, created = GroupTag.objects.get_or_create(name=tag_name)
            group.add_tag(tag)
        return group


class GroupUpdateSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
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


class GroupOwnerUpdateSerializer(serializers.ModelSerializer):
    owner = UserSerializer(many=False, read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    new_owner_pk = serializers.IntegerField(required=True, write_only=True)

    class Meta:
        model = MyGroup
        fields = (
            'pk',
            'name',
            'owner',
            'profile_img',
            'group_type',
            'description',
            'tags',
            'new_owner_pk',

        )
        read_only_fields = (
            'name',
            'owner',
            'profile_img',
            'group_type',
            'description',
            'tags',
        )

    def validate_new_owner_pk(self, new_owner_pk):
        if MyUser.objects.filter(pk=new_owner_pk).exists():
            if self.instance.member.filter(pk=new_owner_pk).exists():
                return new_owner_pk
            else:
                raise serializers.ValidationError('해당 유저는 그룹의 멤버가 아닙니다.')
        else:
            raise serializers.ValidationError('잘못된 유저 pk 값입니다.')

    def update(self, instance, validated_data):
        new_owner_pk = validated_data.get('new_owner_pk')
        new_owner = MyUser.objects.get(pk=new_owner_pk)
        validated_data['owner'] = new_owner
        updated_instance = super().update(instance, validated_data)
        return updated_instance
