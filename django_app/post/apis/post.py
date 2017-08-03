from django.db.models import Q
from rest_framework import generics, permissions, filters
from rest_framework.filters import DjangoFilterBackend

from utils.permissions import ObjectAuthorIsRequestUser
from ..models import Post
from ..serializers import PostSerializer, PostCreateSerializer, PostUpdateSerializer

__all__ = (
    'PostListCreateView',
    'MyPostListCreateView',
    'PostRetrieveUpdateDestroyView',
    'PostConditionalListView'

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
            return Post.objects.filter(group__in=user.group.all())
        else:
            return Post.objects.exclude(group__group_type="HIDDEN")


    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
        ##그룹도 현재 속한 그룹으로 진행 되도록 만들어야한다.

## post 리스트를 조회할 때 사용 (또한, 특정 그룹 및 특정 유저가 작성한 post를 볼때도 사용)
class PostConditionalListView(generics.ListAPIView):
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
    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter)
    filter_fields = ('author', 'group',)
    search_fields = ('content', 'group__name', 'group__description', 'group__tags__name')


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
