from rest_framework import generics, filters, permissions

from ..serializers import TagSerializer
from ..models import GroupTag

__all__ = (
    'TagListView',
)


class TagListView(generics.ListAPIView):
    queryset = GroupTag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
    )
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)