from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.contrib.admin.views.decorators import staff_member_required
import re

from trainingBase.models import TrainingBase, TrainingBaseAdvanced
from my_libs.training_analysis import create_dict_training


@method_decorator(staff_member_required, name='dispatch')
class TrainingBaseView(TemplateView):
    template_name = 'trainingBase/training-base.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    
    
@method_decorator(staff_member_required, name='dispatch')
class SearchTweetsTrainingView(TemplateView):
    template_name = 'trainingBase/search-tweets-training.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        positivo = TrainingBase.objects.filter(sentimento='positivo').count()
        neutro = TrainingBase.objects.filter(sentimento='neutro').count()
        negativo = TrainingBase.objects.filter(sentimento='negativo').count()
        
        alegria = TrainingBaseAdvanced.objects.filter(sentimento='alegria').count()
        nojo = TrainingBaseAdvanced.objects.filter(sentimento='nojo').count()
        medo = TrainingBaseAdvanced.objects.filter(sentimento='medo').count()
        raiva = TrainingBaseAdvanced.objects.filter(sentimento='raiva').count()
        surpresa = TrainingBaseAdvanced.objects.filter(sentimento='surpresa').count()
        tristeza = TrainingBaseAdvanced.objects.filter(sentimento='tristeza').count()
        
        context['trainingBaseSimple'] = positivo, neutro, negativo
        context['trainingBaseAdvanced'] = alegria, nojo, medo, raiva, surpresa, tristeza
        
        return context
    

@method_decorator(staff_member_required, name='dispatch')
class ViewTweetsTrainingView(TemplateView):
    template_name = 'trainingBase/view-tweets-training.html'
    
    def post(self, request, **kwargs):
        
        search_term = request.POST['searched']
        number_of_tweets = request.POST['amoutTweets']
        option = request.POST['inlineRadioOptions']
        tokens = self.request.user.bearerToken
        filter_retweets = True
        
        if search_term:
            tweets = create_dict_training(option, search_term, number_of_tweets, filter_retweets, tokens)
            
            '''
            for tweet in tweets:
                tweet['tweet_clean'] = re.sub(r"\b{}\b".format(search_term), "", tweet['tweet_clean'])
            '''
            
            print(tweets)
            context = super().get_context_data(**kwargs)
            context['tweets'] = tweets
            context['option'] = option
            return render(request, self.template_name, context)
        else:
            messages.success(request, 'Você deve pesquisar algo')
            return redirect('search-tweets-training')
        
        