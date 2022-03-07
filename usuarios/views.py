from django.shortcuts import render
from django.views.generic import TemplateView
from django.urls import reverse_lazy
from django.contrib.auth.models import auth

from .models import CustomUsuario


class CadastroView(TemplateView):
    template_name = 'registration/cadastro.html'
    #form_class = CustomUsuarioCreateForm
    success_url = reverse_lazy('login')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def post(self, request):
        if request.method == 'POST':
            first_name = request.POST['firstname']
            last_name = request.POST['lastname']
            email = request.POST['email']
            password1 = request.POST['password1']
            password2 = request.POST['password2']
            
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
            return render(request, 'index.html')
        
        else:
            return render(request, 'index.html')
    
    
class IndexView(TemplateView):
    template_name = 'index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


# Create your views here.
