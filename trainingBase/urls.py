from django.urls import path
from django.contrib.admin.views.decorators import staff_member_required

from .views import TrainingBaseView, SearchTweetsTrainingView, ViewTweetsTrainingView

urlpatterns = [
    path('training-base/', staff_member_required(TrainingBaseView.as_view()), name='training-base'),
    path('search-tweets-training/', staff_member_required(SearchTweetsTrainingView.as_view()), name='search-tweets-training'),
    path('view-tweets-training/<int:userpk>', staff_member_required(ViewTweetsTrainingView.as_view()), name='view-tweets-training'),
]

