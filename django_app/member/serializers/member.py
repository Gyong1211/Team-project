from rest_framework import serializers

from ..models import MyUser

__all__ = (
    'UserSerializer',
    'UserUpdateSerializer',
    'UserCreateSerializer',
)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = (
            'pk',
            'email',
            'nickname',
            'username',
            'profile_img',
        )

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class UserCreateSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=125)
    nickname = serializers.CharField(max_length=16)
    password1 = serializers.CharField(max_length=24, write_only=True)
    password2 = serializers.CharField(max_length=24, write_only=True)

    def validate_email(self, email):
        if MyUser.objects.filter(email=email).exists():
            raise serializers.ValidationError('존재하는 email 입니다')
        return email

    def validate_nickname(self, nickname):
        if MyUser.objects.filter(nickname=nickname).exists():
            raise serializers.ValidationError('존재하는 nickname 입니다')
        return nickname

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError('password가 일치하지 않습니다')
        return data

    def save(self, *args, **kwargs):
        email = self.validated_data.get('email', '')
        password = self.validated_data.get('password1', '')
        nickname = self.validated_data.get('nickname', '')
        user = MyUser.objects.create_user(
            email=email,
            password=password,
            nickname=nickname,
        )
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    def validate_nickname(self, nickname):
        if MyUser.objects.filter(nickname=nickname).exists():
            raise serializers.ValidationError('이미 존재하는 nickname입니다')
        return nickname

    def validate_username(self, username):
        if MyUser.objects.filter(username=username).exists():
            raise serializers.ValidationError('이미 존재하는 username입니다')

    def validate(self, data):
        if data.get('password1'):
            if data['password1'] != data['password2']:
                raise serializers.ValidationError('password 가 일치하지 않습니다')

        return data

    class Meta:
        model = MyUser
        exclude = (
            'is_staff',
            'is_active',
            'last_login',
        )
        read_only_fields = (
            'date_joined',
        )
