from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib import messages

from .forms import ContatoForm


class AboutView(TemplateView):
    template_name = 'about.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    

class UserOptionsView(TemplateView):
    template_name = 'user_options.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


def ContactView(request):
    form = ContatoForm(request.POST or None)
    if str(request.method) == 'POST':
        if form.is_valid():
            form.send_mail()
            messages.success(request, 'E-mail enviado com sucesso!')
            form = ContatoForm()
        else:
            messages.error(request, 'Erro ao enviar e-mail')
    context = {
        'form': form
    }
    return render(request, 'contact.html', context)
