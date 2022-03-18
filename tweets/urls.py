from django.urls import path

from tweets.views import TakeTweetsView, ViewTweetsView
from .views import ChartData

urlpatterns = [
    path('searchtweets/', TakeTweetsView.as_view(), name='searchtweets'),
    path('viewtweets/', ViewTweetsView.as_view(), name='viewtweets'),
    path('api/chart/data', ChartData.as_view()),
]
