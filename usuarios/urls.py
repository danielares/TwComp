from django.urls import path, include

from .views import IndexView, CadastroView


urlpatterns = [
    path('contas/', include('django.contrib.auth.urls')),
    path('cadastro/', CadastroView.as_view(), name='cadastro'),
    path('', IndexView.as_view(), name='index')
]