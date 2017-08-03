from django.contrib.auth import authenticate
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers


class AuthTokenSerializer(serializers.Serializer):
    email = serializers.CharField(label=_("email"))
    password = serializers.CharField(label=_("Password"), style={'input_type': 'password'})

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(email=email, password=password)

            if user:
                if not user.is_active:
                    msg = '유저의 계정이 비활성화 상태입니다'
                    raise serializers.ValidationError(msg)
            else:
                msg = 'email, password가 일치하지 않습니다'
                raise serializers.ValidationError(msg)
        else:
            msg = '유저가 존재하지 않습니다'
            raise serializers.ValidationError(msg)

        attrs['user'] = user
        return attrs
