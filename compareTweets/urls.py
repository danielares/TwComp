from django.urls import path
from django.contrib.auth.decorators import login_required
from compareTweets.views import ViewCompareTweetsView, CompareTweetsView, CompareChartData
    
urlpatterns = [
    path('search-tweets-compare/', login_required(ViewCompareTweetsView.as_view()), name='search-tweets-compare'),
    path('view-tweets-compare/<int:userpk>/', CompareTweetsView.as_view(), name='view-tweets-compare'),
    path('api/chart/compare-chart-data/<int:userid>/<str:term1>-<str:term2>/', CompareChartData.as_view()),
]