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
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated
                and bool(request.user.is_staff or request.user.role == 'admin')
                )
