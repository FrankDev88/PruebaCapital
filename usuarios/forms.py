# Django
from django import forms

# Models
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.urls import get_resolver
from usuarios.models import Perfil

# Utils
from django_recaptcha.fields import ReCaptchaField
import re
import unicodedata

UserModel = get_user_model()


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label='Username o Email')

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if '@' in username:
            """
            Si el usuario contiene '@',
            considerarlo como un email y validarlo
            """
            try:
                user = UserModel.objects.get(email=username)
            except UserModel.DoesNotExist:
                raise ValidationError(
                    "No se encontró un usuario registrado con este email."
                )
            return user.username
        return username


class SignupForm(forms.Form):
    # Signup Form
    username = forms.CharField(
        label=False,
        min_length=4,
        max_length=20,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Username',
                'onkeyup': 'without_space(this);'
            }
        )
    )
    password = forms.CharField(
        label=False,
        max_length=70,
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'})
    )
    password_confirmation = forms.CharField(
        label=False,
        max_length=70,
        widget=forms.PasswordInput(
            attrs={'placeholder': 'Password confirmation'}
        )
    )
    email = forms.CharField(
        label=False,
        min_length=6,
        max_length=70,
        widget=forms.EmailInput(attrs={'placeholder': 'Email'})
    )

    def clean_username(self):
        username = self.cleaned_data["username"]
        if not username:
            raise ValidationError("El nombre de usuario no puede ser vacío.")
        if len(username) > 20:
            raise forms.ValidationError(
                "El nombre de usuario no puede tener más de 20 caracteres"
            )
        if not re.match("^[a-zA-Z0-9 ]+$", username):
            raise forms.ValidationError(
                "El nombre de usuario tiene que ser alfanumérico"
            )
        if ' ' in username or '/' in username:
            raise forms.ValidationError(
                "El nombre de usuario no puede contener espacios ni '/'"
            )
        username_taken = User.objects.filter(username=username).exists()
        if username_taken:
            raise forms.ValidationError("El nombre de usuario ya está en uso")

        return username

    def clean(self):
        # Verify password confirmation match
        data = super().clean()

        password = data["password"]
        password_confirmation = data["password_confirmation"]

        if password != password_confirmation:
            raise forms.ValidationError("Las contraseñas no coinciden")

        if len(password) < 8:
            raise forms.ValidationError(
                "La contraseña debe tener al menos 8 caracteres y debe "
                "incluir al menos un dígito y una letra mayúscula."
            )

        if not re.search(r'\d', password):
            raise forms.ValidationError(
                "La contraseña debe tener al menos 8 caracteres y debe "
                "incluir al menos un dígito y una letra mayúscula."
            )

        if not re.search(r'[A-Z]', password):
            raise forms.ValidationError(
                "La contraseña debe tener al menos 8 caracteres y debe "
                "incluir al menos un dígito y una letra mayúscula."
            )

        return data

    def save(self):
        # Create user and profile
        data = self.cleaned_data
        data.pop("password_confirmation")

        user = User.objects.create_user(**data)
        profile = Perfil(user=user)
        profile.save()
