from rest_framework import permissions


class IsModers(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='IsModers').exists()


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.owner == request.user:
            return True
        return False
