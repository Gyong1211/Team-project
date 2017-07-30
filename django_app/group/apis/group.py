from django.db.models import Q
from rest_framework import generics

from member.serializers import UserSerializer
from ..serializers import GroupSerializer
from ..models import MyGroup


class GroupListCreateView(generics.ListCreateAPIView):
    serializer_class = GroupSerializer

    def get_queryset(self):
        keyword = self.request.GET.get('search', '')
        if keyword:
            # 멤버 숫자를 Integer 값으로 저장하는 필드 생성 후, 검색 출력 결과를 멤버수로 정렬하도록 .order_by() 추가 필요
            if self.request.user.is_staff:
                return MyGroup.objects.filter(Q(name__contains=keyword) | Q(tags__name__contains=keyword))
            else:
                return MyGroup.objects.exclude(group_type="HIDDEN").filter(
                    Q(name__contains=keyword) | Q(tags__name__contains=keyword)
                )

        else:
            if self.request.user.is_staff:
                return MyGroup.objects.all()
            else:
                return MyGroup.objects.exclude(group_type="HIDDEN")


class GroupRetrieveView(generics.RetrieveAPIView):
    queryset = MyGroup.objects.all()
    serializer_class = GroupSerializer


class GroupMemberListView(generics.ListAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        group_pk = self.kwargs['pk']
        group = MyGroup.objects.get(pk=group_pk)
        return group.members.all()
