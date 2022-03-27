from django.urls import path, include

from usuarios.views import IndexView, CreateUserView

urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    path('', IndexView.as_view(), name='index'),
    path('create-user/', CreateUserView.as_view(), name='create_user'),
]