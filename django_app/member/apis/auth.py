from django.contrib.auth import logout
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import MyUser
from ..serializers import AuthTokenSerializer

__all__ = (
    'LoginView',
    'LogoutView',
)


class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['user']
        user = MyUser.objects.get(email=email)
        token, created = Token.objects.get_or_create(user=email)
        email.last_login = timezone.now()
        email.save(update_fields=['last_login'])
        return Response({'user': user.pk, 'token': token.key})


class LogoutView(APIView):
    def post(self, request, *args, **kwargs):
        return self.logout(request)

    def logout(self, request):
        try:
            request.user.auth_token.delete()
        except (AttributeError, ObjectDoesNotExist):
            return Response("제공된 토큰이 없습니다")
        logout(request)
        return Response("성공적으로 logout 되었습니다")
