from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from member.serializers import UserUpdateSerializer, UserRelationSerializer
from utils.permissions import ObjectIsRequestUser
from ..models import MyUser, UserRelation
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


class UserRelationView(APIView):
    def post(self, request, *args, **kwargs):
        from_user = MyUser.objects.get(pk=request.user.pk)
        to_user_pk = request.data.get('to_user_pk')
        to_user = MyUser.objects.get(pk=to_user_pk)
        if from_user.pk == to_user_pk:
            return Response("본인입니다")
        else:
            UserRelation.objects.create(
                from_user=from_user,
                to_user=to_user,
            )
            return Response("해당 유저를 follow 합니다")

