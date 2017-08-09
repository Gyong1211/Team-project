from django.db.models import Q
from rest_framework import generics, permissions

from utils.permissions import ObjectAuthorIsRequestUser
from ..models import Comment, Post
from ..serializers import CommentSerializer

__all__ = (
    'CommentCreateView',
    'CommentRetrieveUpdateDestroyView',
)


class CommentCreateView(generics.CreateAPIView):
    # def get_queryset(self):
    #     if 'pk' in self.kwargs:
    #         pk = self.kwargs['pk']
    #         Comment.objects.filter(post_set__pk=pk)
    #     else:
    #         None
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        post_pk = self.kwargs['pk']
        serializer.save(author=self.request.user, post=Post.objects.get(pk=post_pk))

    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
    )


class CommentRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    # def get_queryset(self):
    #     if self.request.user.is_authenticated:
    #         return Comment.objects.filter(author=self.request.user)
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        ObjectAuthorIsRequestUser,
    )
