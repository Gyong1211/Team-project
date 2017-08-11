from django.http import Http404
from rest_framework import generics, permissions
from rest_framework.generics import get_object_or_404

from utils.permissions import ObjectAuthorIsRequestUser
from ..models import Comment, Post
from ..serializers import CommentSerializer

__all__ = (
    'CommentListCreateView',
    'CommentRetrieveUpdateDestroyView',
)


class CommentListCreateView(generics.ListCreateAPIView):
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
    )
    serializer_class = CommentSerializer

    def get_queryset(self):
        post_pk = self.kwargs['pk']
        post = get_object_or_404(Post, pk=post_pk)
        return post.comment_set.all()

    def perform_create(self, serializer):
        post_pk = self.kwargs['pk']
        post = get_object_or_404(Post, pk=post_pk)
        serializer.save(author=self.request.user, post=post)


class CommentRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        ObjectAuthorIsRequestUser,
    )
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
