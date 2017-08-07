from django.db.models import Q
from rest_framework import generics, permissions

from utils.permissions import ObjectAuthorIsRequestUser
from ..models import Comment
from ..serializers import CommentSerializer

__all__ = (
    'CommentListCreateView',
    'CommentRetrieveUpdateDestroyView',

)


class CommentListCreateView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Comment.objects.filter(author=self.request.user)

    serializer_class = CommentSerializer

    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        ObjectAuthorIsRequestUser,
    )
