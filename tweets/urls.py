from django.contrib.auth.decorators import login_required
from  django.views.decorators.cache import never_cache
from django.urls import path

from tweets.views import TakeTweetsView, ViewTweetsView, ViewAllTweetsView
from .views import ChartData

urlpatterns = [
    path('search-tweets/', login_required(TakeTweetsView.as_view()), name='search-tweets'),
    path('view-tweets/<int:userid>/', never_cache(ViewTweetsView.as_view()), name='view-tweets'),
    path('view-all-tweets/<int:userid>/', never_cache(ViewAllTweetsView.as_view()), name='view-all-tweets'),
    path('api/chart/data/<int:userid>/<str:term>/', ChartData.as_view()),
]
