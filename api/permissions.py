from rest_framework import permissions


class IsAdmin(permissions.IsAdminUser):
    def has_permission(self, request, view):
        return (request.user.role == 'admin'
                and request.user.is_staff)
