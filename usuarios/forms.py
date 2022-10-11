from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms

from .models import CustomUsuario


class CustomUsuarioCreateForm(UserCreationForm):
    class Meta:
        model = CustomUsuario
        fields = ('first_name', 'last_name', 'username',
                  'bearerToken', 'googleGeocodingApi', 'password1', 'password2')


class CustomUsuarioChangeForm(UserChangeForm):

    class Meta:
        model = CustomUsuario
        fields = ('first_name', 'last_name', 'bearerToken', 'googleGeocodingApi')

