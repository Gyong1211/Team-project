from rest_framework import serializers

from group.models import MyGroup
from group.serializers import GroupSerializer
from .member import UserSerializer
from ..models import Membership, MyUser


class MembershipSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    group = GroupSerializer(read_only=True)
    group_pk = serializers.IntegerField(write_only=True)

    class Meta:
        model = Membership
        fields = (
            'user',
            'group',
            'joined_date',
            'group_pk',
        )
        read_only_fields = (
            'joined_date',
        )

    def validate_group_pk(self, group_pk):
        if not MyGroup.objects.filter(pk=group_pk).exists():
            raise serializers.ValidationError('존재하지 않는 그룹입니다.')
        if Membership.objects.filter(user=self.context['request'].user, group__pk=group_pk):
            raise serializers.ValidationError('이미 가입한 그룹입니다.')
        return group_pk

    def save(self, user):
        group_pk = self.validated_data.pop('group_pk')
        group = MyGroup.objects.get(pk=group_pk)
        super().save(user=user, group=group)
        return self

# class MembershipSerializer(serializers.ModelSerializer):
#     user = UserSerializer(read_only=True)
#     group = GroupSerializer(read_only=True)
#
#     class Meta:
#         model = Membership
#         fields = (
#             'user',
#             'group',
#             'joined_date'
#         )
#         read_only_fields = (
#             'joined_date',
#         )
