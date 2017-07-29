from rest_framework import generics

from member.serializers import UserSerializer
from ..serializers import GroupSerializer
from ..models import MyGroup


class GroupListCreateView(generics.ListCreateAPIView):
    queryset = MyGroup.objects.all()
    serializer_class = GroupSerializer


class GroupRetrieveView(generics.RetrieveAPIView):
    queryset = MyGroup.objects.all()
    serializer_class = GroupSerializer


class GroupMemberListView(generics.ListAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        group_pk = self.kwargs['pk']
        group = MyGroup.objects.get(pk=group_pk)
        return group.members.all()
