from rest_framework import generics, permissions

from utils.permissions import ObjectAuthorIsRequestUser
from ..models import Post
from ..serializers import PostSerializer, PostCreateSerializer, PostUpdateSerializer

__all__ = (
    'PostListCreateView',
    'MyPostListCreateView',
    'PostRetrieveUpdateDestroyView',

)


# 일반 뷰페이지 (내가 속한 그룹의 글만 보여줌)
class PostListCreateView(generics.ListCreateAPIView):
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return PostSerializer
        elif self.request.method == 'POST':
            return PostCreateSerializer

    def get_queryset(self):
        queryset = []
        user = self.request.user
        joined_groups = user.groups_joined.all()
        for joined_group in joined_groups:
            posts_in_group = joined_group.post_set.all()
            for post_in_group in posts_in_group:
                queryset.append(post_in_group)
        return queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


# 개인 포스트 페이지에서 보여질 리스트 및 생성 뷰 (내가 작성한 글만 보여줌)
class MyPostListCreateView(generics.ListCreateAPIView):
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return PostSerializer
        elif self.request.method == 'POST':
            return PostCreateSerializer

    def get_queryset(self):
        user = self.request.user
        return Post.objects.filter(author=user)


class PostRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        ObjectAuthorIsRequestUser,
    )
    serializer_class = PostUpdateSerializer
    # def get_serializer_class(self):
    #     if self.request.method in permissions.SAFE_METHODS:
    #         return PostUpdateSerializer
    #     else:
    #         return PostUpdateSerializer


