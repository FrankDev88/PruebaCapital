# Django
from django.urls import path

# View
from vehiculos import views


urlpatterns = [
    path(
        route="registro_vehiculo",
        view=views.RegisterVehicleView.as_view(),
        name='registro_vehiculo'
    ),
    path(
        route="crear_evento",
        view=views.CreateEventView.as_view(),
        name='crear_evento'
    ),
    path(
        route="crear_invitacion",
        view=views.CreateInvitationView.as_view(),
        name='crear_invitacion'
    ),
    path(
        route="status_invitacion",
        view=views.InvitationStatusView.as_view(),
        name='status_invitacion'
    ),
    path(
        route="get_info",
        view=views.GetInfoView.as_view(),
        name='get_info'
    ),
]
