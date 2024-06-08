# Django REST Framework
from rest_framework import serializers

# Models
from vehiculos.models import Vehiculo, Invitado, Evento

# Serializers
from usuarios.serializers import PerfilSerializer


class VehiculoSerializer(serializers.ModelSerializer):
    """Vehiculo serializer."""
    conductor = PerfilSerializer(read_only=True)

    class Meta:
        """Meta class."""

        model = Vehiculo
        fields = "__all__"


class EventoSerializer(serializers.ModelSerializer):
    """Evento serializer."""
    evento_id = serializers.IntegerField(source="id", required=False)
    dueño = PerfilSerializer(read_only=True)

    class Meta:
        """Meta class."""

        model = Evento
        fields = ["evento_id", "dueño", "nombre", "max_invitados"]


class InvitadoSerializer(serializers.ModelSerializer):
    """Invitado serializer."""
    invitado_id = serializers.IntegerField(source="id", required=False)
    evento_id = serializers.IntegerField(source="evento.id", required=False)
    status = serializers.CharField(required=False)

    hora_entrada_epoch = serializers.SerializerMethodField()
    hora_entrada_iso = serializers.DateTimeField(source="hora_entrada")
    hora_salida_epoch = serializers.SerializerMethodField()
    hora_salida_iso = serializers.DateTimeField(source="hora_salida")

    class Meta:
        """Meta class."""

        model = Invitado
        fields = [
            "invitado_id", "num_placas", "hora_entrada_epoch",
            "hora_entrada_iso", "hora_salida_epoch", "hora_salida_iso",
            "evento_id", "status"
        ]

    def get_hora_entrada_epoch(self, obj):
        if obj.hora_entrada:
            return int(obj.hora_entrada.timestamp())
        else:
            return None

    def get_hora_salida_epoch(self, obj):
        if obj.hora_salida:
            return int(obj.hora_salida.timestamp())
        else:
            return None
