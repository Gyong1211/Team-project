from rest_framework import generics, filters, permissions

from utils import paginations
from ..serializers import TagSerializer
from ..models import GroupTag

__all__ = (
    'TagListView',
)


class TagListView(generics.ListAPIView):
    queryset = GroupTag.objects.all()
    serializer_class = TagSerializer
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    search_fields = ('name',)
    ordering_fields = ('name',)
    pagination_class = paginations.TagListPagination
