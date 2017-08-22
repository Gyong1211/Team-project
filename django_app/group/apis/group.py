from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions, filters, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from utils import paginations
from utils import permissions as custom_permissions
from ..models import MyGroup
from ..serializers import *

__all__ = (
    'GroupListCreateView',
    'GroupRetrieveUpdateDestroyView',
    'GroupOwnerUpdateView',
    'GroupProfileImgDestroyView',
    'MyGroupListView',
)


class GroupListCreateView(generics.ListCreateAPIView):
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
    )
    pagination_class = paginations.GroupListPagination
    filter_backends = (filters.SearchFilter, DjangoFilterBackend,)
    search_fields = ('name', 'description', 'tags__name')
    filter_fields = ('member',)

    def get_queryset(self):
        if self.request.user.is_authenticated:
            if self.request.user.is_staff:
                return MyGroup.objects.all()
            else:
                return MyGroup.objects.exclude(group_type="HIDDEN") | \
                       MyGroup.objects.filter(Q(group_type="HIDDEN") & Q(member=self.request.user))
        else:
            return MyGroup.objects.exclude(group_type="HIDDEN")

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return GroupSerializer
        elif self.request.method == 'POST':
            return GroupCreateSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class GroupRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MyGroup.objects.all()
    permission_classes = (
        custom_permissions.ObjectOwnerIsRequestUserOrReadOnly,
    )

    def get_serializer_class(self):
        if self.request.method in permissions.SAFE_METHODS:
            return GroupSerializer
        else:
            return GroupUpdateSerializer


class GroupOwnerUpdateView(generics.UpdateAPIView):
    queryset = MyGroup.objects.all()
    serializer_class = GroupOwnerUpdateSerializer
    permission_classes = (
        custom_permissions.ObjectOwnerIsRequestUser,
    )


class GroupProfileImgDestroyView(APIView):
    permission_classes = (
        custom_permissions.ObjectOwnerIsRequestUser,
    )

    def get_object(self, pk):
        obj = get_object_or_404(MyGroup, pk=pk)
        self.check_object_permissions(self.request, obj)
        return obj

    def delete(self, *args, **kwargs):
        group = self.get_object(kwargs.get('pk'))
        group.profile_img = None
        group.save()
        return Response({"detail": "그룹의 프로필 이미지가 삭제되었습니다."}, status=status.HTTP_200_OK)


class MyGroupListView(generics.ListAPIView):
    serializer_class = GroupSerializer
    permission_classes = (
        permissions.IsAuthenticated,
    )
    pagination_class = paginations.MyGroupListPagination

    def get_queryset(self):
        user = self.request.user
        return user.group.order_by('-membership')
