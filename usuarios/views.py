from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.models import auth
from django.contrib import messages

from .models import CustomUsuario


class CreateUserView(TemplateView):
    template_name = 'registration/cadastro.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def post(self, request):
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        email = request.POST['email']
        password1 = request.POST['password1']
        
        consumerKey = request.POST['consumerKey']
        consumerSecret = request.POST['consumerSecret']
        accessToken = request.POST['accessToken']
        accessTokenSecret = request.POST['accessTokenSecret']
        bearerToken = request.POST['bearerToken']
        
        usuario = CustomUsuario.objects.create_user(first_name=first_name, 
                                                    last_name=last_name, 
                                                    email=email, 
                                                    password=password1, 
                                                    consumerKey=consumerKey, 
                                                    consumerSecret=consumerSecret, 
                                                    accessToken=accessToken, 
                                                    accessTokenSecret=accessTokenSecret, 
                                                    bearerToken=bearerToken)

        return render(request, 'registration/login.html')
    

class ModifyUserView(TemplateView):
    template_name = 'registration/modificar.html'

    def post(self, request):
        usuario = request.user
        
        usuario.first_name = request.POST['firstname']
        usuario.last_name = request.POST['lastname']
        usuario.email = request.POST['email']
        
        usuario.consumerKey = request.POST['consumerKey']
        usuario.consumerSecret = request.POST['consumerSecret']
        usuario.accessToken = request.POST['accessToken']
        usuario.accessTokenSecret = request.POST['accessTokenSecret']
        usuario.bearerToken = request.POST['bearerToken']
        usuario.save()

        messages.success(request, 'Seu perfil foi atualizado com sucesso!')
        
        return render(request, self.template_name)
        
          
 
class IndexView(TemplateView):
    template_name = 'index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
