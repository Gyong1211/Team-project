from rest_framework import generics, permissions, status, filters
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from member.serializers import UserUpdateSerializer, UserRelationCreateSerializer, UserPasswordUpdateSerializer
from utils.permissions import ObjectIsRequestUser
from utils.permissions.member import ObjectFromUserIsRequestUser
from ..models import MyUser, UserRelation
from ..serializers import UserSerializer, UserCreateSerializer


class UserListCreateView(generics.ListCreateAPIView):
    queryset = MyUser.objects.all()
    filter_backends = (filters.SearchFilter, filters.DjangoFilterBackend)
    search_fields = ('^nickname',)
    filter_fields = ('group',)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return UserSerializer
        elif self.request.method == 'POST':
            return UserCreateSerializer


class UserRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MyUser.objects.all()
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        ObjectIsRequestUser,
    )

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return UserSerializer
        else:
            return UserUpdateSerializer


class UserRelationCreateDestroyView(APIView):
    permission_classes = (
        ObjectFromUserIsRequestUser,
    )

    def get_object(self, from_user_pk, to_user_pk):
        obj = get_object_or_404(UserRelation, from_user=from_user_pk, to_user=to_user_pk)
        self.check_object_permissions(self.request, obj)
        return obj

    def post(self, request, *args, **kwargs):
        serializer = UserRelationCreateSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save(from_user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        relation = self.get_object(request.user.pk, request.data.get('to_user'))
        relation.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserPasswordUpdateView(APIView):
    permission_classes = (
        ObjectIsRequestUser,
    )

    def get_object(self, pk):
        obj = get_object_or_404(MyUser, pk=pk)
        self.check_object_permissions(self.request, obj)
        return obj

    def patch(self, request, *args, **kwargs):
        instance = self.get_object(kwargs.get('pk'))
        serializer = UserPasswordUpdateSerializer(instance=instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": '비밀번호가 변경되었습니다.'}, status=status.HTTP_200_OK)


class FollowerListView(APIView):
    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        user = get_object_or_404(MyUser, pk=pk)
        queryset = MyUser.objects.filter(pk__in=user.follower.all().values('from_user'))
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class FollowingListView(APIView):
    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        user = get_object_or_404(MyUser, pk=pk)
        queryset = MyUser.objects.filter(pk__in=user.following.all().values('to_user'))
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

