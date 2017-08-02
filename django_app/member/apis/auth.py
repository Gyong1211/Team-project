from django.utils import timezone
from rest_framework import parsers, renderers
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from ..serializers import AuthTokenSerializer

__all__ = (
    'LoginView',
    'LogoutView',
)


class LoginView(APIView):
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class = AuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=email)
        email.last_login = timezone.now()
        email.save(update_fields=['last_login'])
        return Response('Login complete')


class LogoutView(APIView):
    def post(self, request):
        request.user.auth_token.delete()
        return Response('Logout complete')
