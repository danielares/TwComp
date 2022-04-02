from django.urls import path
from django.contrib.admin.views.decorators import staff_member_required as staff

from .views import TrainingBaseView, SearchTweetsTrainingView, ViewTweetsTrainingView, TrainingBaseSuccessView

urlpatterns = [
    path('training-base/', staff(TrainingBaseView.as_view()), name='training-base'),
    path('search-tweets-training/', staff(SearchTweetsTrainingView.as_view()), name='search-tweets-training'),
    path('view-tweets-training/<int:userpk>/', staff(ViewTweetsTrainingView.as_view()), name='view-tweets-training'),
    path('view-tweets-training/<int:userpk>/', staff(ViewTweetsTrainingView.as_view()), name='view-tweets-training'),
    path('training-success/<int:userpk>/', staff(TrainingBaseSuccessView.as_view()), name='training-success'),
]

