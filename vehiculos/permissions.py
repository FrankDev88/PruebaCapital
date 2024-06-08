# Django REST Framework
from rest_framework.permissions import BasePermission


class IsEventOwner(BasePermission):
    """Verificar que sea el dueño del Evento."""

    def has_object_permission(self, request, view, obj):
        return request.user.perfil == obj.dueño
