from django.shortcuts import render
from django.views.generic import TemplateView


class AboutView(TemplateView):
    template_name = 'about.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class ContactView(TemplateView):
    template_name = 'contact.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context