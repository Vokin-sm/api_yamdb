from rest_framework import permissions


class IsAdmin(permissions.IsAdminUser):
    """Object-level permission to only allow admins to edit it."""
    def has_permission(self, request, view):
        return request.user.is_admin


class IsAdminOrReadOnly(permissions.BasePermission):
    """Object-level permission to only allow admins to edit it or read only."""

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_admin
        )


class IsOwnerOrAdminOrModeratorOrReadOnly(permissions.BasePermission):
    """Permission to only allow all staff or owner edit it or read only"""
    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or obj.author == request.user
                or request.user.is_staff
                or request.user.is_admin
                or request.user.is_moderator
                )
