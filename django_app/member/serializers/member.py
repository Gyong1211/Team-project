from rest_framework import serializers

from ..models import MyUser, UserRelation

__all__ = (
    'UserSerializer',
    'UserUpdateSerializer',
    'UserCreateSerializer',
    'UserRelationSerializer',
    'UserRelationCreateSerializer',
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
            'group',
        )


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

    def create(self, validated_data):
        password = validated_data.pop('password1', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

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


class UserRelationSerializer(serializers.ModelSerializer):
    from_user = UserSerializer
    to_user = UserSerializer()

    class Meta:
        model = UserRelation
        fields = (
            'from_user',
            'to_user',
        )
        read_only_fields = (
            'created_date',
        )


class UserRelationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRelation
        fields = (
            'from_user',
            'to_user',
        )
        read_only_fields = (
            'from_user',
            'created_date',
        )

    def validate_to_user(self, to_user):
        if self.context['request'].user == to_user:
            raise serializers.ValidationError('본인은 팔로우 할 수 없습니다.')
        elif self.Meta.model.objects.filter(
                from_user=self.context['request'].user,
                to_user=to_user
        ).exists():
            raise serializers.ValidationError('이미 팔로우 중입니다.')
        return to_user