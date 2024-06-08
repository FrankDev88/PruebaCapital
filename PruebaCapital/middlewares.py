# Django
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.deprecation import MiddlewareMixin

# Django REST Framework
from rest_framework.exceptions import AuthenticationFailed

# Utils
import jwt


class CustomAuthMiddleware(MiddlewareMixin):
    def process_request(self, request):
        access_token = request.COOKIES.get('access_token')
        if access_token:
            header_token = f'Bearer {access_token}'
            request.META['HTTP_AUTHORIZATION'] = header_token

            try:
                token = header_token.split(' ')[1]
                payload = jwt.decode(
                    token,
                    settings.SECRET_KEY,
                    algorithms=['HS256']
                )
                user = get_user_model().objects.get(id=payload['user_id'])
                request.user = user
            except (
                jwt.ExpiredSignatureError,
                jwt.InvalidTokenError,
                get_user_model().DoesNotExist
            ):
                raise AuthenticationFailed('Invalid or expired token')


class MethodOverrideMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method == 'POST' and '_method' in request.POST:
            request.method = request.POST['_method']
        response = self.get_response(request)
        return response
