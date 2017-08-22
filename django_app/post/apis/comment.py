from rest_framework import generics, permissions, filters, mixins
from rest_framework.generics import GenericAPIView

from utils import paginations
from utils import permissions as custom_permissions
from ..models import Comment
from ..serializers import CommentSerializer, CommentUpdateSerializer

__all__ = (
    'CommentListCreateView',
    'CommentUpdateDestroyView',
)


class CommentListCreateView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
    )
    pagination_class = paginations.CommentListPagination
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('post',)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentUpdateDestroyView(mixins.UpdateModelMixin, mixins.DestroyModelMixin, GenericAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentUpdateSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        custom_permissions.ObjectAuthorIsRequestUser,
    )

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
