from rest_framework import permissions, status, generics
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import Membership
from ..serializers.membership import MembershipCreateSerializer

__all__ = (
    'MembershipCreateDestroyView',
)


class MembershipCreateDestroyView(APIView):
    permission_classes = (
        permissions.IsAuthenticated,
    )

    def post(self, request):
        serializer = MembershipCreateSerializer(data=request.data, context={"user_pk": request.user.pk})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        if not request.user.pk == int(request.data.get('user_pk')):
            return Response({"user_pk": ["잘못된 유저에 대한 요청입니다."]}, status=status.HTTP_400_BAD_REQUEST)
        group_pk = request.data.get('group_pk')
        membership = get_object_or_404(Membership, user=request.user, group__pk=group_pk)
        if request.user == membership.group.owner:
            return Response({"그룹장은 그룹을 탈퇴할 수 없습니다."}, status=status.HTTP_400_BAD_REQUEST)
        membership.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
