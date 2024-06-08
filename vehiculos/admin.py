# Django
from django.contrib import admin
from django.contrib.auth.models import Group

# Models
from vehiculos.models import Vehiculo, Invitado, Evento
from django.contrib.auth.models import User


@admin.register(Vehiculo)
class VehiculoAdmin(admin.ModelAdmin):
    """Vehiculo admin."""

    list_display = ('id', 'marca', 'modelo', 'num_serie', 'num_placas')
    search_fields = (
        'id', 'marca', 'modelo', 'num_serie',
        'num_placas', 'conductor__user__username'
    )
    list_filter = ('conductor',)


@admin.register(Invitado)
class InvitadoAdmin(admin.ModelAdmin):
    """Invitado admin."""

    list_display = (
        'id', 'num_placas', 'vehiculo',
        'evento', 'hora_entrada', 'hora_salida'
    )
    search_fields = ('id', 'num_placas', 'vehiculo', 'evento')
    list_filter = ('evento',)


@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    """Evento admin."""

    list_display = ('id', 'nombre', 'max_invitados')
    search_fields = ('id', 'nombre')
