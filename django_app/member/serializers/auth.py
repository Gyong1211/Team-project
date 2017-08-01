from django.contrib.auth import authenticate
from rest_framework import serializers

from member.models import MyUser


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(
        max_length=125
    )
    password = serializers.CharField(
        write_only=True
    )

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(email=email, password=password)

            if not user.is_active:
                message = '비활성 계정입니다'
                raise serializers.ValidationError(message, code='authorization')
        else:
            message ='email과 password 가 존재하지 않습니다'
            raise serializers.ValidationError(message, code='authorization')
        attrs['user'] = user
        return attrs
