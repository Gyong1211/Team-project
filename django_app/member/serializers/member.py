from django.contrib.auth import authenticate
from rest_framework import serializers

from ..models import MyUser


class UserSerializer(serializers.ModelSerializer):
    profile_img_url = serializers.SerializerMethodField()

    class Meta:
        model = MyUser
        fields = (
            'pk',
            'email',
            'nickname',
            'username',
            'profile_img_url',
        )

    def get_profile_img_url(self, obj):
        return obj.profile_img.url


class UserUpdateSerializer(serializers.ModelSerializer):
    ori_password = serializers.CharField(
        write_only=True,
        style={'input_type': 'password'},
    )
    password1 = serializers.CharField(
        write_only=True,
        style={'input_type': 'password'},
    )
    password2 = serializers.CharField(
        write_only=True,
        style={'input_type': 'password'},
    )

    class Meta:
        model = MyUser
        fields = (
            'pk',
            'email',
            'nickname',
            'username',
            'profile_img',
            'ori_password',
            'password1',
            'password2',
        )
        read_only_fields = (
            'pk',
            'email',
        )

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError('비밀번호가 다르게 입력되었습니다.')
        return data

    def update(self, instance, validated_data):
        if not authenticate(email=instance.email, password=self.validated_data.get('ori_password', instance.password)):
            raise serializers.ValidationError('기존 비밀번호가 다릅니다.')
        instance.email = self.validated_data.get('email', instance.email)
        instance.nickname = self.validated_data.get('nickname', instance.nickname)
        instance.username = self.validated_data.get('username', instance.username)
        instance.profile_img = self.validated_data.get('profile_img', instance.profile_img)
        instance.set_password(self.validated_data.get('password1', instance.password))
        instance.save()
        return instance


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

    def validate_email(self, email):
        if MyUser.objects.filter(email=email).exists():
            raise serializers.ValidationError('이미 존재하는 이메일입니다.')
        return email

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError('비밀번호가 다르게 입력되었습니다.')
        return data

    def save(self):
        user = MyUser.objects.create_user(
            email=self.validated_data.get('email', ''),
            nickname=self.validated_data.get('nickname', ''),
            password=self.validated_data.get('password1', ''),
            username=self.validated_data.get('username', ''),
        )
        return user
