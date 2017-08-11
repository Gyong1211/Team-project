from rest_framework.pagination import PageNumberPagination

__all__ = (
    'GroupListPagination',
    'TagListPagination',
)


class GroupListPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = page_size


class TagListPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = page_size
