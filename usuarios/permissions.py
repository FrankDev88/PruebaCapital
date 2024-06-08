# Django REST Framework
from rest_framework.permissions import BasePermission


class IsStaff(BasePermission):
    """Verificar que sea Staff."""

    def has_permission(self, request, view):
        return request.user.groups.filter(name="Staff").exists()
