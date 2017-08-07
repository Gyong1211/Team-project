from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from member.serializers import UserUpdateSerializer, UserRelationCreateSerializer
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


class UserRelationView(APIView):

    def post(self, request, *args, **kwargs):
        serializer = UserRelationCreateSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save(from_user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        relation = self.get_object()
        relation.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
