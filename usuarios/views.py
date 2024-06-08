# Django
from django.conf import settings
from django.contrib.auth import authenticate, password_validation
from django.http import HttpResponseRedirect
from django.http.response import JsonResponse
from django.urls import reverse_lazy

# Django REST Framework
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

# Forms
from usuarios.forms import CustomAuthenticationForm, SignupForm


# Vista de Login
class LoginView(TokenObtainPairView):
    # Login View

    template_name = "users/login.html"
    renderer_classes = [JSONRenderer, TemplateHTMLRenderer]
    authentication_form = CustomAuthenticationForm

    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        return Response()

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        # Authenticate the user
        user = authenticate(username=username, password=password)

        if user is not None:
            print(f'Usuario autenticado: {user.username}')  # Debugging line

            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)

            # Call the super() method to get the standard response
            response = super().post(request, *args, **kwargs)

            if response.status_code == status.HTTP_200_OK:
                response.set_cookie(
                    key='access_token',
                    value=access_token,
                    httponly=True,
                    secure=True,
                    samesite='Strict',
                    max_age=settings.ACCESS_TOKEN_EXPIRATION,  # 1 day
                )
                response.set_cookie(
                    key='refresh_token',
                    value=refresh_token,
                    httponly=True,
                    secure=True,
                    samesite='Strict',
                    max_age=settings.ACCESS_TOKEN_EXPIRATION,  # 1 day
                )
                print(f'access_token asignado: {access_token}')
                print(f'refresh_token asignado: {refresh_token}')

                # Redirect to a specific URL after successful login
                redirect_response = HttpResponseRedirect(
                    reverse_lazy('vehiculos:registro_vehiculo')
                )
                redirect_response.set_cookie(
                    key='access_token',
                    value=access_token,
                    httponly=True,
                    secure=True,
                    samesite='Strict',
                    max_age=settings.ACCESS_TOKEN_EXPIRATION,  # 5 minutes
                )
                redirect_response.set_cookie(
                    key='refresh_token',
                    value=refresh_token,
                    httponly=True,
                    secure=True,
                    samesite='Strict',
                    max_age=settings.ACCESS_TOKEN_EXPIRATION,  # 1 day
                )
                if "text/html" in self.request.accepted_media_type:
                    return redirect_response
                else:
                    return response
            else:
                print(f'Error en super() response: {response.status_code}')
                return response
        else:
            # Return error response if authentication fails
            return Response(
                {'mensaje': 'Credenciales Inválidas'},
                status=status.HTTP_401_UNAUTHORIZED
            )


# Vista de Logout
class LogoutView(GenericAPIView):

    def post(self, request):
        try:
            # Obtener el token de refresco del request
            refresh_token = request.COOKIES.get('refresh_token')
            if refresh_token:
                # Invalidar el token de refresco
                token = RefreshToken(refresh_token)
                token.blacklist()
                print(f"Refresh token invalidado: {refresh_token}")
        except Exception as e:
            print(f"Error invalidando token: {e}")

        # Crear la respuesta y eliminar las cookies
        if "text/html" in self.request.headers.get('Accept'):
            response = HttpResponseRedirect(reverse_lazy('usuarios:login'))
        else:
            response = JsonResponse({"mensaje": "Logout exitoso!"}, safe=False)
        response.delete_cookie('access_token', path='/', domain=None)
        response.delete_cookie('refresh_token', path='/', domain=None)
        print("Cookies deleted and user redirected to login")
        return response


# Vista para Registrarse
class SignupView(GenericAPIView):

    template_name = 'users/signup.html'
    renderer_classes = [JSONRenderer, TemplateHTMLRenderer]
    form_class = SignupForm

    def get_context_data(self, **kwargs):
        context = {}

        help_text = password_validation.password_validators_help_text_html()
        context["help_text"] = help_text
        context["form"] = self.form_class
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return Response(context)

    def get_form_kwargs(self):
        kwargs = {}

        if self.request.method in ("POST"):
            kwargs.update(
                {
                    "data": self.request.POST,
                    "files": self.request.FILES,
                }
            )
        return kwargs

    def form_valid(self, form):
        form.save()
        if "text/html" in self.request.accepted_media_type:
            return HttpResponseRedirect(reverse_lazy('usuarios:login'))
        else:
            return JsonResponse({"mensaje": "Usuario creado"})

    def post(self, request, *args, **kwargs):
        form = self.form_class(**self.get_form_kwargs())
        if form.is_valid():
            return self.form_valid(form)

        if "text/html" in self.request.accepted_media_type:
            return Response(self.get_context_data(form=form))
        else:
            return JsonResponse(form.errors)
