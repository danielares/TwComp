from django.contrib.auth.decorators import login_required
from django.urls import path

from tweets.views import TakeTweetsView, ViewTweetsView, ScraperTweetsView, ViewScraperTweetsView
from .views import ChartData

urlpatterns = [
    path('search-tweets/', login_required(TakeTweetsView.as_view()), name='search-tweets'),
    path('search-tweets/results/', ViewTweetsView.as_view(), name='view-tweets'),
    path('search-tweets/api/', ChartData.as_view(), name='tweets-api'),
    
    path('search-tweets-scraper/', ScraperTweetsView.as_view(), name='search-tweets-scraper'),
    path('view-tweets-scraper/', ViewScraperTweetsView.as_view(), name='view-tweets-scraper'),
]
