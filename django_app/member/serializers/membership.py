from rest_framework import serializers

from ..models import Membership


class MembershipCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Membership
        fields = (
            'user',
            'group',
            'joined_date',
        )
        read_only_fields = (
            'user',
            'joined_date',
        )

    def validate_group(self, group):
        if self.Meta.model.objects.filter(user=self.context['request'].user, group=group):
            raise serializers.ValidationError('이미 가입한 그룹입니다.')
        return group
