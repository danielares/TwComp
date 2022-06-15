from django.urls import path

from .views import ContactView, AboutView, UserOptionsView, TestPhraseView, TestResultView, IndexView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('about/', AboutView.as_view(), name='about'),
    path('contact/', ContactView, name='contact'),
    path('test-phrase/', TestPhraseView.as_view(), name='test-phrase'),
    path('test-phrase/result/', TestResultView.as_view(), name='test-result'),
    path('user-options/', UserOptionsView.as_view(), name='user-options')
]