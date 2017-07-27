from rest_framework import generics

from post.models import Comment
from ..models import Post
from ..serializers import PostSerializer

__all__ = (
    'PostListCreateView',
)


class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        instance = serializer.save(author=self.request.user)
        posted_group = self.request.data.get('group')
        if posted_group:
            instance.group = Comment.objects.create(
                post=instance,
                author=instance.author,
                group=posted_group,
            )
            instance.save()
