from unicodedata import name
from django.urls import path, include

from usuarios.views import IndexView, CadastroView
from tweets.views import TakeTweetsView, ViewTweetsView
from compareTweets.views import ViewCompareTweetsView, CompareTweetsView
from .views import chartsView

urlpatterns = [
    path('contas/', include('django.contrib.auth.urls')),
    path('', IndexView.as_view(), name='index'),
    path('cadastro/', CadastroView.as_view(), name='cadastro'),
    path('searchtweets/', TakeTweetsView.as_view(), name='searchtweets'),
    path('viewtweets/', ViewTweetsView.as_view(), name='viewtweets'),
    path('compare-tweets/', ViewCompareTweetsView.as_view(), name='compareTweets'),
    path('view-compare-tweets/', CompareTweetsView.as_view(), name='view-compare-tweets'),
    path('charts/', chartsView.as_view(), name='charts'),
]