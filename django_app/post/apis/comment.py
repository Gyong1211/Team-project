from django.http import Http404
from rest_framework import generics, permissions, filters, status, mixins
from rest_framework.generics import get_object_or_404, GenericAPIView
from rest_framework.response import Response

from utils import paginations
from utils.permissions import ObjectAuthorIsRequestUser
from ..models import Comment, Post
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
    filter_backends = (filters.DjangoFilterBackend, )
    filter_fields = ('post', )
    pagination_class = paginations.CommentListPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentUpdateDestroyView(mixins.UpdateModelMixin, mixins.DestroyModelMixin, GenericAPIView):
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        ObjectAuthorIsRequestUser,
    )
    queryset = Comment.objects.all()
    serializer_class = CommentUpdateSerializer

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
