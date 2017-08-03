from rest_framework import generics, permissions

from member.serializers import UserUpdateSerializer
from utils.permissions import ObjectIsRequestUser
from ..models import MyUser
from ..serializers import UserSerializer, UserCreateSerializer


class UserListCreateView(generics.ListCreateAPIView):
    queryset = MyUser.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return UserSerializer
        elif self.request.method == 'POST':
            return UserCreateSerializer


class UserUpdateView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MyUser.objects.all()
    serializer_class = UserUpdateSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        ObjectIsRequestUser,
    )

    # def get_serializer_class(self):
    #     if self.request.method == 'PATCH':
    #         return UserUpdateSerializer
    #     if self.request.method == 'DELETE':
    #         return UserUpdateSerializer