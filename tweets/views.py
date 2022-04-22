from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.utils.datastructures import MultiValueDictKeyError

from datetime import datetime
import json

from my_libs.word_cloud import wordCloud
from my_libs.return_data_view import get_tweets
from my_libs.scraper import search_tweets_scraper
from my_libs.return_data_view import generate_data, probability_average, get_tweets_to_show


@method_decorator(login_required, name='dispatch')
class TakeTweetsView(TemplateView):
    template_name = 'tweets/search-tweets.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ViewTweetsView(TemplateView):
        template_name = 'tweets/view-tweets.html'
        
        def post(self, request, **kwargs):
            
            options = {}
            options['search'] = request.POST['searched']
            options['number_of_tweets'] = request.POST['amoutTweets']
            options['type_of_analysis'] = request.POST['inlineRadioOptions']
            
            # Opção para incluir mapas
            try: options['option_maps'] = request.POST['includeMaps']
            except: options['option_maps'] = False
            
            # Opção para filtrar retweets
            try: options['filter_retweets'] = bool(request.POST['filterRetweets'])
            except MultiValueDictKeyError: options['filter_retweets'] = False
            
            # Opção para filtrar respostas
            try: options['filter_reply'] = bool(request.POST['filterReply'])
            except MultiValueDictKeyError: options['filter_reply'] = False
            
            # if para veficiar se o usuario fez alguma pesquisa
            if not options['search']:
                messages.error(request, 'Você deve pesquisar algo')
                return redirect('search-tweets')
                
            api_access_tokens = self.request.user.bearerToken
            charts_info, context_infos = get_tweets(api_access_tokens, options) 
            word_cloud_image = wordCloud(context_infos['tweets'], options['search'])  
                      
            request.session['search'] = options['search']
            request.session['options'] = json.dumps(options, indent=4, sort_keys=True, default=str)
            request.session['number_of_tweets'] = options['number_of_tweets']
            request.session['charts_info'] = charts_info
            request.session['tweets'] = json.dumps(context_infos['tweets'], indent=4, sort_keys=True, default=str)
            
            request.session.modified = True
            
            context = super().get_context_data(**kwargs)
            context['context_infos'] = context_infos
            context['chartsInfo'] = charts_info
            context['wordcloud'] = word_cloud_image
            context['locations'] = context_infos['geo_location']
            
            return render(request, self.template_name, context)


class ScraperTweetsView(TemplateView):
        template_name = 'webscraper/search-tweets-scraper.html'
        
        def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            return context
   
        
class ViewScraperTweetsView(TemplateView):
        template_name = 'webscraper/view-tweets-scraper.html'
        
        def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            return context
        
        def post(self, request, **kwargs):
            options = {}
            options['search'] = request.POST['searched']
            options['number_of_tweets'] = int(request.POST['amoutTweets'])
            options['type_of_analysis'] = request.POST['inlineRadioOptions']
            
            if not options['search']:
                messages.error(request, 'Você deve pesquisar algo')
                return redirect('search-tweets-scraper') 
            
            tweets = search_tweets_scraper(options)
            charts_info = generate_data(tweets, options['type_of_analysis'])
            probability = probability_average(tweets)
            word_cloud_image = wordCloud(tweets, options['search'])
            tweets_to_show = get_tweets_to_show(tweets)
            
            request.session['search'] = options['search']
            request.session['options'] = json.dumps(options, indent=4, sort_keys=True, default=str)
            request.session['number_of_tweets'] = options['number_of_tweets']
            request.session['charts_info'] = charts_info
            request.session['tweets'] = json.dumps(tweets, indent=4, sort_keys=True, default=str)
            request.session.modified = True
            
            context_infos = {
                'options': {
                    'search': options['search'],
                    'type_of_analysis': options['type_of_analysis'],
                    'number_of_tweets': options['number_of_tweets'],
                },
                'tweets': tweets,
                'probability': round(probability, 2),
                'tweets_to_show': tweets_to_show,
                'data_time': datetime.today()
            }
            
            context = super().get_context_data(**kwargs)
            context['context_infos'] = context_infos
            context['chartsInfo'] = charts_info
            context['wordcloud'] = word_cloud_image

            return render(request, self.template_name, context)