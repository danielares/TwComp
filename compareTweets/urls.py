from django.urls import path
from django.contrib.auth.decorators import login_required
from compareTweets.views import ViewCompareTweetsView, CompareTweetsView, ScraperTweetsCompareView, ViewScraperTweetsCompareView
    
urlpatterns = [
    path('search-tweets-compare/', login_required(ViewCompareTweetsView.as_view()), name='search-tweets-compare'),
    path('view-tweets-compare/', CompareTweetsView.as_view(), name='view-tweets-compare'),
    path('search-tweets-compare-scraper/', ScraperTweetsCompareView.as_view(), name='search-tweets-compare-scraper'),
    path('view-tweets-compare-scraper/', ViewScraperTweetsCompareView.as_view(), name='view-tweets-compare-scraper'),
]