from django.contrib.auth.decorators import login_required
from django.urls import path

from tweets.views import TakeTweetsView, ViewTweetsView, ViewAllTweetsView
from .views import ChartData

urlpatterns = [
    path('search-tweets/', login_required(TakeTweetsView.as_view()), name='search-tweets'),
    path('view-tweets/<int:userid>/', ViewTweetsView.as_view(), name='view-tweets'),
    path('view-all-tweets/<int:userid>/', ViewAllTweetsView.as_view(), name='view-all-tweets'),
    path('api/chart/data/<int:userid>/<str:term>/', ChartData.as_view()),
]
