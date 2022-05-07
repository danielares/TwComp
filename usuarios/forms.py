from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms

from .models import CustomUsuario


class CustomUsuarioCreateForm(UserCreationForm):
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()
    consumerKey = forms.EmailField()
    consumerSecret = forms.EmailField()
    accessToken = forms.EmailField()
    accessTokenSecret = forms.EmailField()
    bearerToken = forms.EmailField()

    class Meta:
        model = CustomUsuario
        fields = ('first_name', 'last_name', 'email', 'consumerKey', 'consumerSecret', 'accessToken', 'accessTokenSecret', 'bearerToken')

        widgets = {
            'email': forms.EmailInput(attrs={'class':'input', 'placeholder': 'Email Address'}),
        }


class CustomUsuarioChangeForm(UserChangeForm):

    class Meta:
        model = CustomUsuario
        fields = ('first_name', 'last_name', 'consumerKey', 'consumerSecret', 'accessToken', 'accessTokenSecret', 'bearerToken')

