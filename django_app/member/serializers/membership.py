from rest_framework import serializers

from group.models import MyGroup
from group.serializers import GroupSerializer
from .member import UserSerializer
from ..models import Membership, MyUser


# class MembershipCreateSerializer(serializers.ModelSerializer):
#     user = UserSerializer(read_only=True)
#     group = GroupSerializer(read_only=True)
#     user_pk = serializers.IntegerField(required=True, write_only=True)
#     group_pk = serializers.IntegerField(required=True, write_only=True)
#
#     class Meta:
#         model = Membership
#         fields = (
#             'user',
#             'group',
#             'user_pk',
#             'group_pk',
#         )
#
#     def validate_user_pk(self, user_pk):
#         if user_pk != self.context['user_pk']:
#             raise serializers.ValidationError('잘못된 유저에 대한 요청입니다.')
#         return user_pk
#
#     def validate_group_pk(self, group_pk):
#         if not MyGroup.objects.filter(pk=group_pk).exists():
#             raise serializers.ValidationError('존재하지 않는 그룹입니다.')
#         return group_pk
#
#     def validate(self, data):
#         user = MyUser.objects.get(pk=data['user_pk'])
#         group = MyGroup.objects.get(pk=data['group_pk'])
#         if Membership.objects.filter(user=user, group=group).exists():
#             raise serializers.ValidationError('이미 가입한 그룹입니다.')
#         return data
#
#     def create(self, validated_data):
#         user = MyUser.objects.get(pk=validated_data.get('user_pk'))
#         group = MyGroup.objects.get(pk=validated_data.get('group_pk'))
#         return Membership.objects.create(user=user, group=group)

class MembershipSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    group = GroupSerializer(read_only=True)

    class Meta:
        model = Membership
        fields = (
            'user',
            'group',
            'joined_date'
        )
        read_only_fields = (
            'joined_date',
        )
