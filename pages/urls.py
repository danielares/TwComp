from django.urls import path

from .views import AboutView, ContactView

urlpatterns = [
    path('about/', AboutView.as_view(), name='about'),
    path('contact/', ContactView, name='contact'),
]