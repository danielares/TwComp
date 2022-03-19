from django.urls import path

from .views import GeneratePdfView, GenerateCsvView

urlpatterns = [
    path('generate-pdf/', GeneratePdfView.as_view(), name='generate-pdf'),
    path('generate-csv/', GenerateCsvView.as_view(), name='generate-csv'),
]
