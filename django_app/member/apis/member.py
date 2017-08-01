from django.utils.datastructures import MultiValueDictKeyError
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import MyUser
from ..serializers import UserSerializer, UserCreationSerializer


class UserListCreateView(generics.ListCreateAPIView):
    queryset = MyUser.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return UserSerializer
        elif self.request.method == 'POST':
            return UserCreationSerializer


class UserProfileView(APIView):
    def patch(self, request, *args, **kwargs):
        user = request.user
        try:
            for request_item in request.data.keys():
                if request_item not in [item for item in UserSerializer(user).fields]:
                    return Response(status=status.HTTP_400_BAD_REQUEST, data={"detail": "data 타입이 잘못되었습니다"})
            nickname = request.data.get("nickname", False)
            if MyUser.objects.filter(nickname=nickname).exists():
                return Response(status=status.HTTP_400_BAD_REQUEST, data={"detail": "해당 nickname 을 다른 유저가 사용중입니다"})
            else:
                return Response(status=status.HTTP_200_OK, data=UserSerializer(user).data)
        except MultiValueDictKeyError:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"detail": "잘못된 형식의 data 입니다"})

    def delete(self, request, format=None):
        user = request.user
        # user 가 자신의 profile 로 들어가서 삭제버튼을 눌러야만 삭제할 수 있다.
        user.delete()
        ret = {
            "detail": "유저가 삭제되었습니다."
        }
        return Response(ret)
