from django.urls import path

from .views import ChartData

urlpatterns = [
    path('api/chart/data', ChartData.as_view())
]
