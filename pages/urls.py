from django.urls import path

from .views import AboutView, ContactView, UserOptionsView, TestPhraseView, TestResultView

urlpatterns = [
    path('about/', AboutView.as_view(), name='about'),
    path('contact/', ContactView, name='contact'),
    path('test-phrase/', TestPhraseView.as_view(), name='test-phrase'),
    path('test-result/<int:userpk>', TestResultView.as_view(), name='test-result'),
    path('user-options/<int:userpk>', UserOptionsView.as_view(), name='user_options')
]