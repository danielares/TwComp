from django.shortcuts import render
from django.views.generic import TemplateView

class CompareTweetsView(TemplateView):
    template_name = 'compareTweets/compare-tweets.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
