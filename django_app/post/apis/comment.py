from django.db.models import Q
from django.http import Http404
from rest_framework import generics, permissions
from rest_framework.generics import get_object_or_404

from utils.permissions import ObjectAuthorIsRequestUser
from ..models import Comment, Post
from ..serializers import CommentSerializer

__all__ = (
    'CommentCreateView',
    'CommentRetrieveUpdateDestroyView',
)


class CommentCreateView(generics.CreateAPIView):
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
    )

    def get_queryset(self):
        post_pk = self.kwargs['pk']
        return Comment.objects.filter(post__pk=post_pk)

    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        post_pk = self.kwargs['pk']
        try:
            serializer.save(author=self.request.user, post=Post.objects.get(pk=post_pk))
        except Post.objects.filter(pk=post_pk).model.DoesNotExist:
            raise Http404(
                'No %s matches the given query.' % Post.objects.filter(pk=post_pk).model._meta.object_name)


class CommentRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        ObjectAuthorIsRequestUser,
    )
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
