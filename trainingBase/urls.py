from django.urls import path

from .views import TrainingBaseView

urlpatterns = [
    path('training-base/', TrainingBaseView.as_view(), name='training-base'),
]

