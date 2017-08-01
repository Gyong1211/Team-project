from rest_framework import generics, permissions, filters

from utils.permissions import ObjectOwnerIsRequestUser
from ..serializers import GroupSerializer, GroupCreateSerializer, GroupUpdateSerializer
from ..models import MyGroup


class GroupListCreateView(generics.ListCreateAPIView):
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'description', 'tags__name')

    def get_queryset(self):
        if self.request.user.is_staff:
            return MyGroup.objects.all()
        else:
            return MyGroup.objects.exclued(group_type="HIDDEN")

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
