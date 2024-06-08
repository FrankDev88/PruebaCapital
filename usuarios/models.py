# Django
from django.contrib.auth.models import User
from django.db import models


class Perfil(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    biografia = models.TextField(blank=True, null=True)
    telefono = models.CharField(max_length=12, blank=True, null=True)
    foto = models.ImageField(
        upload_to="users/pictures",
        blank=True,
        null=True,
        max_length=500
    )

    verificado = models.BooleanField(blank=True, null=True)

    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        # Retorna el username
        return self.user.username

    class Meta:
        verbose_name_plural = "Perfiles"
