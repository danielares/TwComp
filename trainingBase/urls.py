from django.urls import path
from django.contrib.admin.views.decorators import staff_member_required as staff

from .views import TrainingBaseView, SearchTweetsTrainingView, ViewTweetsTrainingView, TrainingBaseSuccessView
from .views import UploadBaseView, generateCsvTrainingBase


urlpatterns = [
    path('training-base/', staff(TrainingBaseView.as_view()), name='training-base'),
    path('upload-training-base/', staff(UploadBaseView.as_view()), name='upload-training-base'),
    path('search-tweets-training/', staff(SearchTweetsTrainingView.as_view()), name='search-tweets-training'),
    path('view-tweets-training/', staff(ViewTweetsTrainingView.as_view()), name='view-tweets-training'),
    path('training-success/', staff(TrainingBaseSuccessView.as_view()), name='training-success'),
    path('generate-csv-training-base/', generateCsvTrainingBase, name='generate-csv-training-base'),
]

