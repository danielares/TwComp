from django.urls import path

from .views import GeneratePdfView, GenerateComparePdfView, GenerateCsvView

urlpatterns = [
    path('generate-pdf/', GeneratePdfView.as_view(), name='generate-pdf'),
    path('generate-compare-pdf/', GenerateComparePdfView.as_view(), name='generate-compare-pdf'),
    path('generate-csv/', GenerateCsvView.as_view(), name='generate-csv'),
]
