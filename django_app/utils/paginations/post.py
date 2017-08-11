from rest_framework.pagination import PageNumberPagination

__all__ = (
    'PostListPagination',
)


class PostListPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = page_size
