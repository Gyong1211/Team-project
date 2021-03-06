from django.db.models import Q
from rest_framework import generics, permissions, filters, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from member.models import MyUser
from utils import paginations, permissions as custom_permissions
from ..models import Post
from ..serializers import PostSerializer, PostCreateSerializer, PostUpdateSerializer, UserSerializer

__all__ = (
    'MyGroupPostListView',
    'PostListCreateView',
    'PostRetrieveUpdateDestroyView',
    'PostLikeToggleView',
    'PostLikeUserListView',

)


class PostListCreateView(generics.ListCreateAPIView):
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
    )
    pagination_class = paginations.PostListPagination
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
        custom_permissions.ObjectAuthorIsRequestUser,
    )

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return PostSerializer
        else:
            return PostUpdateSerializer

    def get_queryset(self):
        if self.request.user.is_authenticated:
            if self.request.user.is_staff:
                return Post.objects.all()
            else:
                return Post.objects.exclude(group__group_type="HIDDEN") | \
                       Post.objects.filter(Q(group__group_type="HIDDEN") & Q(author=self.request.user))
        else:
            return Post.objects.exclude(group__group_type="HIDDEN")


class MyGroupPostListView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = (
        permissions.IsAuthenticated,
    )
    pagination_class = paginations.PostListPagination

    def get_queryset(self):
        user = self.request.user
        return Post.objects.filter(group__in=user.group.all())


class PostLikeToggleView(APIView):
    permission_classes = (
        permissions.IsAuthenticated,
    )

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        post_like, post_like_created = post.postlike_set.get_or_create(user=request.user)

        if not post_like_created:
            post_like.delete()

        content = {
            'like_or_not': post_like_created
        }
        return Response(content, status=status.HTTP_200_OK)


class PostLikeUserListView(generics.ListAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        post_pk = self.kwargs['pk']
        return MyUser.objects.filter(postlike__post__pk=post_pk)
