# Django
from django.db.models import Case, When, CharField, Value
from django.http import HttpResponseRedirect
from django.http.response import JsonResponse
from django.urls import reverse_lazy

# Django REST Framework
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.response import Response

# Models
from vehiculos.models import Vehiculo, Invitado, Evento

# Permissions
from usuarios.permissions import IsStaff
from vehiculos.permissions import IsEventOwner

# Serializers
from vehiculos.serializers import (
    VehiculoSerializer,
    EventoSerializer,
    InvitadoSerializer
)

# Utils
import datetime


# Vista de la pantalla para Registrar Vehículos
class RegisterVehicleView(GenericAPIView):
    template_name = 'vehiculos/registro.html'
    renderer_classes = [JSONRenderer, TemplateHTMLRenderer]

    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Método Get: pasa todo el contexto necesario para la vista."""
        return Response()

    def post(self, request):
        """Método Post: maneja la creación del vehiculo."""

        r = request.POST
        marca = r.get("marca")
        modelo = r.get("modelo")
        num_serie = r.get("num_serie")
        num_placas = r.get("num_placas")

        vehiculo = Vehiculo.objects.create(
            marca=marca,
            modelo=modelo,
            num_serie=num_serie,
            num_placas=num_placas,
            conductor=self.request.user.perfil,
        )

        Invitado.objects.filter(
            num_placas=vehiculo.num_placas
        ).update(vehiculo=vehiculo)

        if "text/html" in self.request.accepted_media_type:
            return HttpResponseRedirect(
                reverse_lazy('vehiculos:registro_vehiculo')
            )
        else:
            return JsonResponse(VehiculoSerializer(vehiculo).data, safe=False)


# Vista de la pantalla para Crear Evento
class CreateEventView(GenericAPIView):
    template_name = 'vehiculos/crear_evento.html'
    renderer_classes = [JSONRenderer, TemplateHTMLRenderer]

    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Método Get: pasa todo el contexto necesario para la vista."""
        return Response()

    def post(self, request):
        """Método Post: maneja la creación del evento."""

        r = request.POST
        nombre = r.get("nombre")
        max_invitados = r.get("max_invitados")

        evento = Evento.objects.create(
            nombre=nombre,
            dueño=self.request.user.perfil,
            max_invitados=max_invitados,
        )

        if "text/html" in self.request.accepted_media_type:
            return HttpResponseRedirect(reverse_lazy('vehiculos:crear_evento'))
        else:
            return JsonResponse(EventoSerializer(evento).data, safe=False)


# Vista de la pantalla para Crear Invitación
class CreateInvitationView(GenericAPIView):
    template_name = 'vehiculos/crear_invitacion.html'
    renderer_classes = [JSONRenderer, TemplateHTMLRenderer]

    permission_classes = [IsAuthenticated, IsEventOwner]

    def get_context_data(self, **kwargs):
        context = {}

        eventos = Evento.objects.filter(dueño=self.request.user.perfil)
        context["eventos"] = EventoSerializer(eventos, many=True).data
        return context

    def get(self, request):
        """Método Get: pasa todo el contexto necesario para la vista."""
        context = self.get_context_data()
        return Response(context)

    def post(self, request):
        """Método Post: maneja la creación del invitación."""

        r = request.POST
        num_placas = r.get("num_placas")
        evento_id = r.get("evento_id")

        invitado = Invitado.objects.create(
            num_placas=num_placas,
            evento=Evento.objects.get(id=evento_id),
        )

        try:
            vehiculo = Vehiculo.objects.get(num_placas=num_placas)
            invitado.vehiculo = vehiculo
            invitado.save()
        except Vehiculo.DoesNotExist:
            pass

        if "text/html" in self.request.accepted_media_type:
            return HttpResponseRedirect(
                reverse_lazy('vehiculos:crear_invitacion')
            )
        else:
            return JsonResponse(InvitadoSerializer(invitado).data, safe=False)


# Vista de la pantalla para Invitation Status
class InvitationStatusView(GenericAPIView):
    template_name = 'vehiculos/status_invitacion.html'
    renderer_classes = [JSONRenderer, TemplateHTMLRenderer]
    permission_classes = [IsAuthenticated, IsStaff]

    def get_context_data(self, **kwargs):
        context = {}
        eventos = Evento.objects.all()
        context["eventos"] = eventos
        return context

    def get(self, request):
        """Método Get: pasa todo el contexto necesario para la vista."""
        context = self.get_context_data()
        return Response(context)

    def patch(self, request):
        """Método Patch: maneja el check in y check out."""
        r = request.POST
        invitado_id = r.get("invitado_id")
        accion = r.get("accion")
        invitado = Invitado.objects.get(id=invitado_id)
        if accion == "check_in":
            if not (invitado.hora_entrada) and not (invitado.hora_salida):
                invitado.hora_entrada = datetime.datetime.now()
        if accion == "check_out":
            if invitado.hora_entrada and not (invitado.hora_salida):
                invitado.hora_salida = datetime.datetime.now()
        invitado.save()

        return JsonResponse(InvitadoSerializer(invitado).data, safe=False)


# Vista de la pantalla para Obtener Invitaciones
class GetInfoView(GenericAPIView):
    renderer_classes = [JSONRenderer]
    permission_classes = [IsAuthenticated, IsStaff]

    def get_vehiculo_info(self, **kwargs):
        num_placas = self.request.GET.get("num_placas")

        vehiculo = Vehiculo.objects.get(num_placas=num_placas)
        invitaciones = Invitado.objects.filter(
            vehiculo=vehiculo
        ).annotate(status=Case(
            When(hora_entrada__isnull=False,
                 hora_salida__isnull=False, then=Value("finish")),
            When(hora_entrada__isnull=False, then=Value("check_out")),
            default=Value("check_in"),
            output_field=CharField(),
        ))
        return vehiculo, invitaciones

    def get_invitados(self, **kwargs):
        evento_id = self.request.GET.get("evento_id")
        search = self.request.GET.get("search")

        invitados = Invitado.objects.filter(
            evento=evento_id
        ).annotate(status=Case(
                When(hora_entrada__isnull=False,
                     hora_salida__isnull=False, then=Value("finish")),
                When(hora_entrada__isnull=False, then=Value("check_out")),
                default=Value("check_in"),
                output_field=CharField(),
            ),
        )
        if search:
            invitados = invitados.filter(num_placas__icontains=search)
        return invitados

    def get_eventos(self, **kwargs):
        search = self.request.GET.get("search")
        eventos = Evento.objects.all()
        if search:
            eventos = eventos.filter(nombre__icontains=search)
        return eventos

    def get(self, request):
        """Método Get: pasa todo el contexto necesario para la vista."""
        modelo = self.request.GET.get("modelo")
        if modelo == "vehiculo":
            vehiculo, invitaciones = self.get_vehiculo_info()
            vehiculo_serializer = VehiculoSerializer(vehiculo)
            invitaciones_serializer = InvitadoSerializer(
                invitaciones,
                many=True
            )
            return JsonResponse(
                {
                    "vehiculo": vehiculo_serializer.data,
                    "invitaciones": invitaciones_serializer.data
                },
                safe=False
            )
        elif modelo == "invitado":
            invitados = self.get_invitados()
            invitados_serializer = InvitadoSerializer(invitados, many=True)
            return JsonResponse(invitados_serializer.data, safe=False)
        elif modelo == "evento":
            eventos = self.get_eventos()
            eventos_serializer = EventoSerializer(eventos, many=True)
            return JsonResponse(eventos_serializer.data, safe=False)
