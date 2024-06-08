# Django REST Framework
from rest_framework import serializers

# Models
from usuarios.models import Perfil


class PerfilSerializer(serializers.ModelSerializer):
    """Perfil serializer."""
    username = serializers.CharField(source="user.username", read_only=True)
    first_name = serializers.CharField(
        source="user.first_name",
        read_only=True
    )
    last_name = serializers.CharField(source="user.last_name", read_only=True)
    email = serializers.CharField(source="user.email", read_only=True)

    class Meta:
        """Meta class."""

        model = Perfil
        fields = ["username", "first_name", "last_name", "email"]
