from rest_framework import permissions


class IsAdmin(permissions.IsAdminUser):
    """Object-level permission to only allow admins to edit it."""

    def has_permission(self, request, view):
        return bool(
            request.user
            and (request.user.is_staff
                 or request.user.role == 'admin')
        )


class IsAdminOrReadOnly(permissions.BasePermission):
    """Object-level permission to only allow admins to edit it or read only."""

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated and request.user.is_admin
        )


class IsOwnerOrAdminOrModeratorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or obj.author == request.user
                or request.user.is_staff
                or request.user.role == 'admin'
                or request.user.role == 'moderator'
                )
