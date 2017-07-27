from rest_framework import serializers

from ..models import GroupTag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupTag
        fields = (
            'name',
        )