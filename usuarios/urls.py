from django.urls import path, include

from usuarios.views import IndexView, CadastroView

urlpatterns = [
    path('contas/', include('django.contrib.auth.urls')),
    path('', IndexView.as_view(), name='index'),
    path('cadastro/', CadastroView.as_view(), name='cadastro'),
]