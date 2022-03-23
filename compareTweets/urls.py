from django.urls import path
from compareTweets.views import ViewCompareTweetsView, CompareTweetsView, CompareChartData
    
urlpatterns = [
    path('compare-tweets/', ViewCompareTweetsView.as_view(), name='compareTweets'),
    path('view-compare-tweets/', CompareTweetsView.as_view(), name='view-compare-tweets'),
    path('api/chart/compare-chart-data/', CompareChartData.as_view(), name='api-compare'),
]