from django.shortcuts import render
from django.views.generic import TemplateView


class TrainingBaseView(TemplateView):
    template_name = 'trainingBase/training-base.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        return context