from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib import messages

from .forms import ContatoForm
from my_libs.training_analysis import analyze_test_phrase


class IndexView(TemplateView):
    template_name = 'index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


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


class TestPhraseView(TemplateView):
    template_name = 'testPhrase/test-phrase.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class TestResultView(TemplateView):
    template_name = 'testPhrase/test-result.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    
    def post(self, request, **kwargs):
        phrase = request.POST['phrase']
        option = request.POST['inlineRadioOptions']
        
        if not phrase:
            messages.error(request, 'Você deve digitar uma frase')
            return redirect('test-phrase')
        
        sentiment = analyze_test_phrase(phrase, option)
        
        context = super().get_context_data(**kwargs)
        context['sentiment'] = sentiment
        context['phrase'] = phrase
        
        return render(request, self.template_name, context)


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