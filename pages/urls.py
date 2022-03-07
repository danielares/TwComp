from django.urls import path, include

from usuarios.views import IndexView, CadastroView
from tweets.views import TakeTweetsView, ViewTweetsView


urlpatterns = [
    path('contas/', include('django.contrib.auth.urls')),
    path('', IndexView.as_view(), name='index'),
    path('cadastro/', CadastroView.as_view(), name='cadastro'),
    path('searchtweets/', TakeTweetsView.as_view(), name='searchtweets'),
    path('viewtweets/', ViewTweetsView.as_view(), name='viewtweets'),
]