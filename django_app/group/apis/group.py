from django.db.models import Q
from rest_framework import generics, permissions, filters

from utils.permissions import ObjectOwnerIsRequestUser
from ..serializers import *
from ..models import MyGroup

__all__ = (
    'GroupListCreateView',
    'GroupRetrieveUpdateDestroyView',
    'GroupOwnerUpdateView',
)


class GroupListCreateView(generics.ListCreateAPIView):
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'description', 'tags__name')
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
    )

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
        permissions.IsAuthenticatedOrReadOnly,
        ObjectOwnerIsRequestUser,
    )

    def get_serializer_class(self):
        if self.request.method in permissions.SAFE_METHODS:
            return GroupSerializer
        else:
            return GroupUpdateSerializer


class GroupOwnerUpdateView(generics.UpdateAPIView):
    queryset = MyGroup.objects.all()
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        ObjectOwnerIsRequestUser,
    )
    serializer_class = GroupOwnerUpdateSerializer
