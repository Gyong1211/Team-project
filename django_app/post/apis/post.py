from django.db.models import Q
from rest_framework import generics, permissions, filters

from utils.permissions import ObjectAuthorIsRequestUser
from ..models import Post
from ..serializers import PostSerializer, PostCreateSerializer, PostUpdateSerializer

__all__ = (
    'MyGroupPostListView',
    'PostListCreateView',
    'PostRetrieveUpdateDestroyView',

)


##  내가 속한 그룹의 Post List
class MyGroupPostListView(generics.ListAPIView):
    serializer_class = PostSerializer

    # pagination_class = PostPagination

    def get_queryset(self):
        if self.request.user.is_authenticated:
            user = self.request.user
            return Post.objects.filter(group__in=user.group.all())
        else:
            return None

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


## 범용적 post list create
class PostListCreateView(generics.ListCreateAPIView):
    def get_queryset(self):
        if self.request.user.is_authenticated:
            if self.request.user.is_staff:
                return Post.objects.all()
            else:
                return Post.objects.exclude(group__group_type="HIDDEN") | \
                       Post.objects.filter(Q(group__group_type="HIDDEN") & Q(author=self.request.user))
        else:
            return Post.objects.exclude(group__group_type="HIDDEN")

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return PostSerializer
        elif self.request.method == 'POST':
            return PostCreateSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter)
    filter_fields = ('author', 'group',)
    search_fields = ('content',)


class PostRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    def get_queryset(self):
        if self.request.user.is_authenticated:
            if self.request.user.is_staff:
                return Post.objects.all()
            else:
                return Post.objects.exclude(group__group_type="HIDDEN") | \
                       Post.objects.filter(Q(group__group_type="HIDDEN") & Q(author=self.request.user))
        else:
            return Post.objects.exclude(group__group_type="HIDDEN")

    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        ObjectAuthorIsRequestUser,
    )

    def get_serializer_class(self):
        if self.request.method in permissions.SAFE_METHODS:
            return PostSerializer
        else:
            return PostUpdateSerializer
