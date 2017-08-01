from rest_framework import parsers, renderers
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.response import Response
from rest_framework.views import APIView

from config.settings import AUTH_USER_MODEL
from ..serializers import LoginSerializer



User = AUTH_USER_MODEL

__all__ = (
    'AuthTokenView',
)


class AuthTokenView(APIView):
    throttle_classes = ()
    permissions_classes = ()
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser)
    renderer_classes = (renderers.JSONRenderer)
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})


auth_token = AuthTokenView.as_view()
