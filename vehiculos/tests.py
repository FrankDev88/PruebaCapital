# Django
from django.test import TestCase
from django.urls import reverse

# Django REST Framework
from rest_framework.test import APIClient

# Models
from django.contrib.auth.models import User
from vehiculos.models import Vehiculo, Evento, Invitado
from usuarios.models import Perfil

# Utils
import datetime


class RegisterVehicleViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser', password='testpass'
        )
        self.perfil = Perfil.objects.create(user=self.user)
        self.client.force_authenticate(user=self.user)
        self.url = reverse('vehiculos:registro_vehiculo')

    def test_register_vehicle(self):
        data = {
            "marca": "Toyota",
            "modelo": "Corolla",
            "num_serie": "123ABC",
            "num_placas": "XYZ789"
        }
        response = self.client.post(self.url, data, format='multipart')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Vehiculo.objects.count(), 1)
        vehiculo = Vehiculo.objects.first()
        self.assertEqual(vehiculo.marca, "Toyota")
        self.assertEqual(vehiculo.modelo, "Corolla")
        self.assertEqual(vehiculo.num_serie, "123ABC")
        self.assertEqual(vehiculo.num_placas, "XYZ789")
        self.assertEqual(vehiculo.conductor, self.perfil)


class CreateEventViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass'
        )
        self.perfil = Perfil.objects.create(user=self.user)
        self.client.force_authenticate(user=self.user)
        self.url = reverse('vehiculos:crear_evento')

    def test_create_event(self):
        data = {
            "nombre": "Fiesta",
            "max_invitados": 100
        }
        response = self.client.post(self.url, data, format='multipart')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Evento.objects.count(), 1)
        evento = Evento.objects.first()
        self.assertEqual(evento.nombre, "Fiesta")
        self.assertEqual(evento.dueño, self.perfil)
        self.assertEqual(evento.max_invitados, 100)


class CreateInvitationViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass'
        )
        self.perfil = Perfil.objects.create(user=self.user)
        self.client.force_authenticate(user=self.user)
        self.evento = Evento.objects.create(
            nombre="Evento Test",
            dueño=self.perfil, max_invitados=50
        )
        self.url = reverse('vehiculos:crear_invitacion')

    def test_create_invitation(self):
        data = {
            "num_placas": "XYZ789",
            "evento_id": self.evento.id
        }
        response = self.client.post(self.url, data, format='multipart')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Invitado.objects.count(), 1)
        invitado = Invitado.objects.first()
        self.assertEqual(invitado.num_placas, "XYZ789")
        self.assertEqual(invitado.evento, self.evento)
