from rest_framework import permissions

__all__ = (
    'ObjectOwnerIsRequestUser',
    'ObjectOwnerIsRequestUserOrReadOnly'
)


class ObjectOwnerIsRequestUser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class ObjectOwnerIsRequestUserOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user
