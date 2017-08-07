from rest_framework import permissions

__all__ = (
    'ObjectIsRequestUser',
    'ObjectGroupOwnerIsNotRequestUser',
)


class ObjectIsRequestUser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj == request.user


class ObjectGroupOwnerIsNotRequestUser(permissions.BasePermission):
    message = '그룹장은 탈퇴할 수 없습니다.'

    def has_object_permission(self, request, view, obj):
        return obj.group.owner != request.user
