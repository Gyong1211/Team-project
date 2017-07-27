from rest_framework import generics

from ..serializers import GroupSerializer
from ..models import MyGroup


class GroupListCreateView(generics.ListCreateAPIView):
    queryset = MyGroup.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return GroupSerializer
