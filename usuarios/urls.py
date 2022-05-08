from django.urls import path, include
from django.contrib.auth.decorators import login_required

from usuarios.views import IndexView, CreateUserView, ModifyUserView

urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    path('', IndexView.as_view(), name='index'),
    path('create-user/', CreateUserView.as_view(), name='create-user'),
    path('modify-user/<int:pk>', login_required(ModifyUserView.as_view()), name='modify-user'),
]