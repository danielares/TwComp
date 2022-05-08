from django.views.generic import TemplateView
from django.contrib.auth.models import auth
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import redirect, render
from django.contrib import messages

from .forms import CustomUsuarioCreateForm
from .models import CustomUsuario


class CreateUserView(CreateView):
    form_class = CustomUsuarioCreateForm
    template_name = 'registration/cadastro.html'
    success_url = reverse_lazy('login')
    

@method_decorator(login_required, name='dispatch')
class ModifyUserView(UpdateView):
    model = CustomUsuario
    template_name = 'registration/modificar.html'
    fields = ['first_name', 'last_name', 'username', 'bearerToken']
    success_url = reverse_lazy('index')
    
    def get(self, request, *args, **kwargs):
        user_id = int(self.request.user.id)
        user_id_path_url = int(self.request.get_full_path().split('/')[2])
        if user_id != user_id_path_url:
            return redirect('/modify-user/' + str(user_id))
        else:
            return super().get(request, *args, **kwargs)
    
    def post(self, request, **kwargs):
        user_id = int(self.request.user.id)
        user_id_path_url = int(self.request.get_full_path().split('/')[2])
        
        if user_id == user_id_path_url:
            user = request.user
            user.first_name = request.POST['first_name']
            user.last_name = request.POST['last_name']
            user.username = request.POST['username']
            user.bearerToken = request.POST['bearerToken']
            user.save()
            messages.success(request, 'Seu perfil foi atualizado com sucesso!')
        else:
            messages.warning(request, 'Você não tem autorização para isso.')
        
        return render(request, 'index.html')

 
class IndexView(TemplateView):
    template_name = 'index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
