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


# class MembershipCreateDestroyView(APIView):
#     permission_classes = (
#         permissions.IsAuthenticated,
#     )
#
#     def post(self, request):
#         serializer = MembershipCreateSerializer(data=request.data, context={"user_pk": request.user.pk})
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def delete(self, request):
#         if not request.user.pk == int(request.data.get('user_pk')):
#             return Response({"user_pk": ["잘못된 유저에 대한 요청입니다."]}, status=status.HTTP_400_BAD_REQUEST)
#         group_pk = request.data.get('group_pk')
#         membership = get_object_or_404(Membership, user=request.user, group__pk=group_pk)
#         if request.user == membership.group.owner:
#             return Response({"그룹장은 그룹을 탈퇴할 수 없습니다."}, status=status.HTTP_400_BAD_REQUEST)
#         membership.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

class MembershipCreateDestroyView(generics.GenericAPIView):
    serializer_class = MembershipSerializer
    permission_classes = (
        permissions.IsAuthenticated,
        RequestUserIsNotObjectOwner,

    )

    def get_object(self, group_pk):
        obj = get_object_or_404(Membership, user=self.request.user, group__pk=group_pk)
        self.check_object_permissions(self.request, obj)
        return obj

    def post(self, request, group_pk, *args, **kwargs):
        if Membership.objects.filter(user=request.user, group__pk=group_pk):
            return Response({"detail": "이미 가입한 그룹입니다."}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer, group_pk)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer, group_pk):
        group = get_object_or_404(MyGroup, pk=group_pk)
        serializer.save(user=self.request.user, group=group)

    def delete(self, request, group_pk):
        membership = self.get_object(group_pk)
        membership.delete()
        return Response({"detail": ["그룹을 탈퇴했습니다."]}, status=status.HTTP_204_NO_CONTENT)
