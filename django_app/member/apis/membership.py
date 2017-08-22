from rest_framework import permissions, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from utils import permissions as custom_permissions
from ..models import Membership
from ..serializers.membership import MembershipCreateSerializer

__all__ = (
    'MembershipCreateDestroyView',
)


class MembershipCreateDestroyView(APIView):
    permission_classes = (
        permissions.IsAuthenticated,
        custom_permissions.ObjectGroupOwnerIsNotRequestUser,
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
