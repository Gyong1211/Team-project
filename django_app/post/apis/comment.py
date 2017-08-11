from django.http import Http404
from rest_framework import generics, permissions, filters
from rest_framework.generics import get_object_or_404

from utils import paginations
from utils.permissions import ObjectAuthorIsRequestUser
from ..models import Comment, Post
from ..serializers import CommentSerializer

__all__ = (
    'CommentListCreateView',
    'CommentRetrieveUpdateDestroyView',
)


class CommentListCreateView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    filter_backends = (filters.DjangoFilterBackend, )
    filter_fields = ('post', )
    pagination_class = paginations.CommentListPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        ObjectAuthorIsRequestUser,
    )
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
