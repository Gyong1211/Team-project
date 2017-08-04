from django.http import Http404
from rest_framework import permissions, status, generics, mixins
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from group.models import MyGroup
from utils.permissions import ObjectGroupOwnerIsNotRequestUser
from ..models import Membership
from ..serializers.membership import MembershipSerializer, MembershipCreateSerializer

__all__ = (
    'MembershipCreateDestroyView',
)


# class MembershipCreateDestroyView(APIView):
#     permission_classes = (
#         permissions.IsAuthenticated,
#         ObjectGroupOwnerIsNotRequestUser,
#     )
#
#     def get_object(self):
#         group_pk = self.request.data.get('group_pk')
#         obj = get_object_or_404(Membership, user=self.request.user, group__pk=group_pk)
#         self.check_object_permissions(self.request, obj)
#         return obj
#
#     def post(self, *args, **kwargs):
#         serializer = MembershipSerializer(data=self.request.data, context={"request": self.request})
#         serializer.is_valid(raise_exception=True)
#         serializer.save(user=self.request.user)
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#
#     def delete(self, *args, **kwargs):
#         membership = self.get_object()
#         membership.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


class MembershipCreateDestroyView(APIView):
    permission_classes = (
        permissions.IsAuthenticated,
        ObjectGroupOwnerIsNotRequestUser,
    )

    def get_object(self):
        group = self.request.data.get('group')
        obj = get_object_or_404(Membership, user=self.request.user, group=group)
        self.check_object_permissions(self.request, obj)
        return obj

    def post(self, *args, **kwargs):
        serializer = MembershipCreateSerializer(data=self.request.data, context={"request": self.request})
        serializer.is_valid(raise_exception=True)
        serializer.save(user=self.request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, *args, **kwargs):
        membership = self.get_object()
        membership.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
