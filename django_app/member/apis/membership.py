from django.http import Http404
from rest_framework import permissions, status, generics, mixins
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from group.models import MyGroup
from utils.permissions import RequestUserIsNotObjectOwner
from ..models import Membership
from ..serializers.membership import MembershipSerializer

__all__ = (
    'MembershipCreateDestroyView',
)


class MembershipCreateDestroyView(APIView):
    permission_classes = (
        permissions.IsAuthenticated,
        RequestUserIsNotObjectOwner,
    )

    def get_object(self):
        group_pk = self.request.data.get('group_pk')
        obj = get_object_or_404(Membership, user=self.request.user, group__pk=group_pk)
        self.check_object_permissions(self.request, obj)
        return obj

    def post(self, *args, **kwargs):
        serializer = MembershipSerializer(data=self.request.data, context={"request": self.request})
        serializer.is_valid(raise_exception=True)
        serializer.save(user=self.request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, *args, **kwargs):
        membership = self.get_object()
        membership.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# class MembershipCreateDestroyView(generics.GenericAPIView):
#     serializer_class = MembershipSerializer
#     permission_classes = (
#         permissions.IsAuthenticated,
#         RequestUserIsNotObjectOwner,
#
#     )
#
#     def get_object(self, group_pk):
#         obj = get_object_or_404(Membership, user=self.request.user, group__pk=group_pk)
#         self.check_object_permissions(self.request, obj)
#         return obj
#
#     def post(self, request, group_pk, *args, **kwargs):
#         if Membership.objects.filter(user=request.user, group__pk=group_pk):
#             return Response({"detail": "이미 가입한 그룹입니다."}, status=status.HTTP_400_BAD_REQUEST)
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         self.perform_create(serializer, group_pk)
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#
#     def perform_create(self, serializer, group_pk):
#         group = get_object_or_404(MyGroup, pk=group_pk)
#         serializer.save(user=self.request.user, group=group)
#
#     def delete(self, request, group_pk):
#         membership = self.get_object(group_pk)
#         membership.delete()
#         return Response({"detail": ["그룹을 탈퇴했습니다."]}, status=status.HTTP_204_NO_CONTENT)
