from django.urls import path

from .views import GeneratePdfView, GenerateComparePdfView, generateCsv, generateCsvCompare

urlpatterns = [
    path('generate-pdf/', GeneratePdfView.as_view(), name='generate-pdf'),
    path('generate-compare-pdf/', GenerateComparePdfView.as_view(), name='generate-compare-pdf'),
    path('generateCsv/', generateCsv, name='generate-csv'),
    path('generate-compare-csv/', generateCsvCompare, name='generate-compare-csv'),
    
]
