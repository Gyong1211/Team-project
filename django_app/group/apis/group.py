from django.db.models import Q
from rest_framework import generics

from member.serializers import UserSerializer
from ..serializers import GroupSerializer, GroupCreateSerializer
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


class GroupRetrieveView(generics.RetrieveAPIView):
    queryset = MyGroup.objects.all()
    serializer_class = GroupSerializer


class GroupMemberListView(generics.ListAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        group_pk = self.kwargs['pk']
        group = MyGroup.objects.get(pk=group_pk)
        return group.member.all()
