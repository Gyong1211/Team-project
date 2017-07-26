from rest_framework import serializers

from ..models import MyUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = (
            'pk',
            'email',
            'nickname',
            'username',
            'is_staff'
        )


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = (
            'pk',
            'email',
            'nickname',
            'username',
            'ori_password',
            'password1',
            'password2',
        )


class UserCreationSerializer(serializers.Serializer):
    email = serializers.EmailField(
        max_length=255
    )
    nickname = serializers.CharField(
        max_length=16,
    )
    username = serializers.CharField(
        max_length=12,
    )
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    def validate_nickname(self, nickname):
        if MyUser.objects.filter(nickname=nickname).exists():
            raise serializers.ValidationError('이미 존재하는 닉네임입니다.')
        return nickname

    def validate_password(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError('비밀번호가 다르게 입력되었습니다.')
        return data

    def validate_email(self, email):
        if MyUser.objects.filter(email=email).exists():
            raise serializers.ValidationError('이미 존재하는 이메일입니다.')
        return email

    def save(self):
        email = self.validated_data.get('email', '')
        nickname = self.validated_data.get('nickname', '')
        password = self.validated_data.get('password1', '')
        username = self.validated_data.get('username', '')
        user = MyUser.objects.create_user(
            email=email,
            nickname=nickname,
            password=password,
            username=username,
        )
        return user
