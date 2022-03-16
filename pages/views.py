from django.shortcuts import render
from django.views.generic import TemplateView


class chartsView(TemplateView):
    template_name = 'charts/chart2.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context