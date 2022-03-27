from django.urls import path

from .views import AboutView, ContactView, UserOptionsView

urlpatterns = [
    path('about/', AboutView.as_view(), name='about'),
    path('contact/', ContactView, name='contact'),
    path('user-options/<int:userpk>', UserOptionsView.as_view(), name='user_options')
]