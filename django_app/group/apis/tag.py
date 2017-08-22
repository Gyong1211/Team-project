from rest_framework import generics, filters

from utils import paginations
from ..models import GroupTag
from ..serializers import TagSerializer

__all__ = (
    'TagListView',
)


class TagListView(generics.ListAPIView):
    queryset = GroupTag.objects.all()
    serializer_class = TagSerializer
    pagination_class = paginations.TagListPagination
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    search_fields = ('name',)
    ordering_fields = ('name',)
