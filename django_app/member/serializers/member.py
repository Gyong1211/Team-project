from rest_framework import serializers

from ..models import MyUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = (
            'pk',
            'username',
            'email',
            'nickname',
            'is_staff'
        )


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = (
            'pk',
            'username',
            'email',
            'nickname',
            'ori_password',
            'password1',
            'password2',
        )


class UserCreationSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=15,
    )
    nickname = serializers.CharField(
        max_length=100,
    )
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True)

    def validate_nickname(self, nickname):
        if MyUser.objects.filter(nickname=nickname).exists():
            raise serializers.ValidationError('Nickname already exists')
        return nickname

    def validate_password(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError('Passwords didn\'t match')
        return data

    def validate_email(self, email):
        if MyUser.objects.filter(email=email).exists():
            raise serializers.ValidationError('Email already exists')
        return email

    def save(self):
        username = self.validated_data.get('username', '')
        nickname = self.validated_data.get('nickname', '')
        password = self.validated_data.get('password1', '')
        email = self.validated_data.get('email', '')
        user = MyUser.objects._create_user(
            username=username,
            nickname=nickname,
            password=password,
            email=email,
        )
        return user
