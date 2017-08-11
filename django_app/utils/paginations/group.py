from rest_framework.pagination import PageNumberPagination

__all__ = (
    'GroupListPagination',
    'MyGroupListPagination',
    'TagListPagination',
)


class GroupListPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = page_size


class MyGroupListPagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = page_size


class TagListPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = page_size
