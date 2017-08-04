from rest_framework import permissions


class ObjectIsRequestUser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj == request.user


class ObjectOwnerIsRequestUser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class ObjectOwnerIsRequestUserOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user


class ObjectGroupOwnerIsNotRequestUser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.group.owner != request.user
