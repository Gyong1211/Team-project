from django.db.models import Q
from rest_framework import generics, permissions

from member.serializers import UserSerializer
from post.serializers import PostSerializer
from utils.permissions import ObjectOwnerIsRequestUser
from ..serializers import GroupSerializer, GroupCreateSerializer, GroupUpdateSerializer
from ..models import MyGroup


class GroupListCreateView(generics.ListCreateAPIView):
    def get_queryset(self):
        keyword_list = self.request.GET.get('search', '')
        if keyword_list:
            if self.request.user.is_staff:
                result_queryset = MyGroup.objects.all()
                for keyword in keyword_list.split():
                    result_queryset = result_queryset.filter(
                        Q(name__contains=keyword) | Q(description__contains=keyword) | Q(tags__name__contains=keyword)
                    ).order_by('-num_of_members')
                return result_queryset
            else:
                result_queryset = MyGroup.objects.exclude(group_type="HIDDEN")
                for keyword in keyword_list.split():
                    result_queryset = result_queryset.filter(
                        Q(name__contains=keyword) | Q(description__contains=keyword) | Q(tags__name__contains=keyword)
                    ).order_by('-num_of_members')
                return result_queryset
        else:
            if self.request.user.is_staff:
                return MyGroup.objects.all()
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
