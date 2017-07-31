from rest_framework import generics

from post.models import Comment
from ..models import Post
from ..serializers import PostSerializer, PostCreateSerializer

__all__ = (
    'PostListCreateView',
)


class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return PostSerializer
        elif self.request.method == 'POST':
            return PostCreateSerializer

