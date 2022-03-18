from django.urls import path

from tweets.views import TakeTweetsView, ViewTweetsView
from .views import ChartData, ChartDataPolarity

urlpatterns = [
    path('searchtweets/', TakeTweetsView.as_view(), name='searchtweets'),
    path('viewtweets/', ViewTweetsView.as_view(), name='viewtweets'),
    path('api/chart/data', ChartData.as_view()),
    path('api/chart/data-polarity', ChartDataPolarity.as_view()),
]
