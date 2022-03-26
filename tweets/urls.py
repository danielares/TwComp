from unicodedata import name
from django.urls import path

from tweets.views import TakeTweetsView, ViewTweetsView, ViewAllTweetsView
from .views import ChartData

urlpatterns = [
    path('searchtweets/', TakeTweetsView.as_view(), name='searchtweets'),
    path('viewtweets/<int:userid>/', ViewTweetsView.as_view(), name='viewtweets'),
    path('view-all-tweets/<int:userid>/', ViewAllTweetsView.as_view(), name='view-all-tweets'),
    path('api/chart/data/', ChartData.as_view()),
]
