from rest_framework import permissions

__all__ = (
    'ObjectAuthorIsRequestUser',
)


class ObjectAuthorIsRequestUser(permissions.BasePermission):
    message = '글쓴이만 요청할 수 있는 작업입니다.'

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user
