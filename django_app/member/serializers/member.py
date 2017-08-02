from django.contrib.auth import authenticate
from rest_framework import serializers

from ..models import MyUser

__all__ = (
    'UserSerializer',
    'UserUpdateSerializer',
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


class UserUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = MyUser
        exclude = (
            'is_staff',
            'is_active',
            'last_login',
            'password',
        )
        read_only_fields = (
            'date_joined',
        )


#
#
# class UserUpdateSerializer(serializers.ModelSerializer):
#     ori_password = serializers.CharField(
#         write_only=True,
#         style={'input_type': 'password'},
#     )
#     password1 = serializers.CharField(
#         write_only=True,
#         style={'input_type': 'password'},
#     )
#     password2 = serializers.CharField(
#         write_only=True,
#         style={'input_type': 'password'},
#     )
#
#     class Meta:
#         model = MyUser
#         fields = (
#             'pk',
#             'email',
#             'nickname',
#             'username',
#             'profile_img',
#             'ori_password',
#             'password1',
#             'password2',
#         )
#         read_only_fields = (
#             'pk',
#             'email',
#         )
#
#     def validate(self, data):
#         password1 = self.password1.is_valid()
#         password2 = self.password2.is_valid()
#         if data['password1'] != data['password2']:
#             raise serializers.ValidationError('비밀번호가 다르게 입력되었습니다.')
#     #     return data
#
#     def update(self, instance, validated_data):
#         if not authenticate(email=instance.email, password=validated_data('ori_password')):
#             raise ValueError('기존 비밀번호가 틀립니다.')
#         instance.set_password(validated_data('password1'))
#         instance.save()
#         return instance


    # def update(self, request, validated_data):
    #     # if not authenticate(email=request.email, password=self.validated_data.get('ori_password', request.password)):
    #     #     raise serializers.ValidationError('기존 비밀번호가 다릅니다.')
    #
    #     email = request.get_email()
    #     nickname = request.get_nickname()
    #     username = request.get_username()
    #     profile_img = request.get_profile_img()
    #
    #     return super(UserUpdateSerializer, self).__init__(email, nickname,username, profile_img)

#
# class UserCreationSerializer(serializers.Serializer):
#     email = serializers.EmailField(
#         max_length=255
#     )
#     nickname = serializers.CharField(
#         max_length=16,
#     )
#     username = serializers.CharField(
#         max_length=12,
#     )
#     password1 = serializers.CharField(write_only=True)
#     password2 = serializers.CharField(write_only=True)
#
#     def validate_nickname(self, nickname):
#         if MyUser.objects.filter(nickname=nickname).exists():
#             raise serializers.ValidationError('이미 존재하는 닉네임입니다.')
#         return nickname
#
#     def validate_email(self, email):
#         if MyUser.objects.filter(email=email).exists():
#             raise serializers.ValidationError('이미 존재하는 이메일입니다.')
#         return email
#
#     def validate(self, data):
#         if data['password1'] != data['password2']:
#             raise serializers.ValidationError('비밀번호가 다르게 입력되었습니다.')
#         return data
#
#     def save(self):
#         user = MyUser.objects.create_user(
#             email=self.validated_data.get('email', ''),
#             nickname=self.validated_data.get('nickname', ''),
#             password=self.validated_data.get('password1', ''),
#             username=self.validated_data.get('username', ''),
#         )
#         return user
