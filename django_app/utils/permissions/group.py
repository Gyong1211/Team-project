from rest_framework import permissions

__all__ = (
    'ObjectOwnerIsRequestUser',
    'ObjectOwnerIsRequestUserOrReadOnly'
)


class ObjectOwnerIsRequestUser(permissions.BasePermission):
    message = '그룹장만 접근할 수 있습니다.'

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class ObjectOwnerIsRequestUserOrReadOnly(permissions.BasePermission):
    message = '그룹장 외에는 변경할 수 없습니다.'

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user
