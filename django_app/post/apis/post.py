from django.db.models import Q
from rest_framework import generics, permissions
from rest_framework.filters import DjangoFilterBackend

from utils.permissions import ObjectAuthorIsRequestUser
from ..models import Post
from ..serializers import PostSerializer, PostCreateSerializer, PostUpdateSerializer

__all__ = (
    'PostListCreateView',
    'MyPostListCreateView',
    'PostRetrieveUpdateDestroyView',
    'PostSearchListView'

)


## 메인 페이지 Post List (내가 속한 모든 그룹내의 포스트만 보여줌)
class PostListCreateView(generics.ListCreateAPIView):
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return PostSerializer
        elif self.request.method == 'POST':
            return PostCreateSerializer

    def get_queryset(self):
        if self.request.user.is_authenticated:
            user = self.request.user
            return Post.objects.filter(group__in=user.groups_joined.all())
        else:
            return Post.objects.all()
        return Post.objects.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostSearchListView(generics.ListAPIView):
    def get_queryset(self):
        if self.request.user.is_authenticated:
            if self.request.user.is_staff:
                return Post.objects.all()
            else:
                return Post.objects.exclude(group__group_type="HIDDEN") | \
                       Post.objects.filter(Q(group__group_type="HIDDEN") & Q(author=self.request.user))
        else:
            return Post.objects.exclude(group__group_type="HIDDEN")

    serializer_class = PostSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('author', 'group',)


# 개인 포스트 페이지에서 보여질 리스트 및 생성 뷰 (내가 작성한 글만 보여줌)
class MyPostListCreateView(generics.ListCreateAPIView):
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return PostSerializer
        elif self.request.method == 'POST':
            return PostCreateSerializer

    def get_queryset(self):
        if self.request.user.is_authenticated:
            user = self.request.user
            return Post.objects.filter(author=user)
        else:
            return None

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
        ## 리퀘스트 유저가 있으면 내것만 보이게 없으면 다 보이게


class PostRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        ObjectAuthorIsRequestUser,
    )
    serializer_class = PostUpdateSerializer

    def get_serializer_class(self):
        if self.request.method in permissions.SAFE_METHODS:
            return PostSerializer
        else:
            return PostUpdateSerializer
