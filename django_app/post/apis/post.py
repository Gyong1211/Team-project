from django.db.models import Q
from rest_framework import generics, permissions, filters
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from utils.permissions import ObjectAuthorIsRequestUser
from ..models import Post, PostLike
from ..serializers import PostSerializer, PostCreateSerializer, PostUpdateSerializer

__all__ = (
    'MyGroupPostListView',
    'PostListCreateView',
    'PostRetrieveUpdateDestroyView',
    'PostLikeToggle',

)


#  내가 속한 그룹의 Post List
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


# 범용적 post list create
class PostListCreateView(generics.ListCreateAPIView):
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
    )
    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter)
    filter_fields = ('author', 'group',)
    search_fields = ('content',)

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


class PostRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        ObjectAuthorIsRequestUser,
    )

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
        if self.request.method in permissions.SAFE_METHODS:
            return PostSerializer
        else:
            return PostUpdateSerializer


class PostLikeToggle(APIView):
    permission_classes = (
        permissions.IsAuthenticated,
    )

    def get(self, request, post_pk):
        post = get_object_or_404(Post, pk=post_pk)
        post_like, post_like_created = post.postlike_set.get_or_create(user=request.user)

        if not post_like_created:
            post_like.delete()
            post.like_count -= 1

        elif post_like_created:
            post.like_count += 1

        post.save()
        content = {
            'like_or_not': post_like_created
        }
        return Response(content)
