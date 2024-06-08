# Django
from django.core.exceptions import ValidationError
from django.db import models


class Vehiculo(models.Model):

    marca = models.CharField(max_length=255)
    modelo = models.CharField(max_length=255)
    num_serie = models.CharField(max_length=255)
    num_placas = models.CharField(max_length=255, unique=True)
    conductor = models.ForeignKey(
        "usuarios.Perfil",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.marca} {self.modelo} - {self.num_placas}"


class Invitado(models.Model):

    num_placas = models.CharField(max_length=255)
    vehiculo = models.ForeignKey(
        "Vehiculo",
        on_delete=models.SET_NULL,
        related_name='invitaciones',
        null=True,
        blank=True
    )
    evento = models.ForeignKey(
        "Evento",
        on_delete=models.CASCADE,
        related_name='invitados'
    )

    hora_entrada = models.DateTimeField(null=True, blank=True)
    hora_salida = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.num_placas} - {self.evento}"

    def clean(self):
        if self.evento.invitados.count() >= self.evento.max_invitados:
            raise ValidationError(
                "La lista de invitados ha alcanzado su "
                "número máximo de invitados."
            )
        
        misma_invitacion = self.evento.invitados.filter(
            num_placas=self.num_placas
        ).exclude(pk=self.pk)

        if misma_invitacion.exists():
            raise ValidationError(
                "Ya existe una invitación con estas placas en el mismo evento."
            )


class Evento(models.Model):
    nombre = models.CharField(max_length=255)
    dueño = models.ForeignKey("usuarios.Perfil", on_delete=models.CASCADE)
    max_invitados = models.PositiveIntegerField(default=100)

    def __str__(self):
        return self.nombre
