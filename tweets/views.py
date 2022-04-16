from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.contrib import messages
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.utils.datastructures import MultiValueDictKeyError

from my_libs.word_cloud import wordCloud
from my_libs.return_data_view import get_tweets
from my_libs.training_analysis import search_tweets_scraper
from my_libs.return_data_view import generate_data, probability_average


@method_decorator(login_required, name='dispatch')
class TakeTweetsView(TemplateView):
    template_name = 'tweets/search-tweets.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ViewTweetsView(TemplateView):
        template_name = 'tweets/view-tweets.html'
        
        def post(self, request, **kwargs):
            global api
            
            search = request.POST['searched']
            number_of_tweets = request.POST['amoutTweets']
            option = request.POST['inlineRadioOptions']
            
            # Opção para incluir mapas
            try: option_maps = request.POST['includeMaps']
            except: option_maps = False
            
            # Opção para filtrar retweets
            try: filter_retweets = bool(request.POST['filterRetweets'])
            except MultiValueDictKeyError: filter_retweets = False
            
            # Opção para filtrar respostas
            try: filter_reply = bool(request.POST['filterReply'])
            except MultiValueDictKeyError: filter_reply = False
            
            # if para veficiar se o usuario fez alguma pesquisa
            if not search:
                messages.error(request, 'Você deve pesquisar algo')
                return redirect('search-tweets')
                
            tokens = self.request.user.bearerToken
            tweets, charts_info, probability, geo_locations = get_tweets(search, number_of_tweets, option, filter_retweets, 
                                                                            filter_reply, option_maps, tokens) 
            word_cloud_image = wordCloud(tweets, search)
            
            api = {"term": search, "amoutTweets": number_of_tweets, 
                    "chartsInfo": charts_info, 'tweets': tweets}

            context = super().get_context_data(**kwargs)
            context['chartsInfo'] = charts_info
            context['wordcloud'] = word_cloud_image
            context['option'] = option
            context['term'] = search
            context['tweets'] = tweets
            context['probability'] = round(probability, 2)
            context['amoutTweets'] = number_of_tweets
            context['locations'] = geo_locations
            return render(request, self.template_name, context)
                
        def return_api_data():
            global api
            return api


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
            search = request.POST['searched']
            number_of_tweets = int(request.POST['amoutTweets'])
            option = request.POST['inlineRadioOptions']
            
            if not search:
                messages.error(request, 'Você deve pesquisar algo')
                return redirect('search-tweets-scraper') 
            
            tweets = search_tweets_scraper(search, number_of_tweets, option)
            charts_info = generate_data(tweets, option)
            probability = probability_average(tweets)
            word_cloud_image = wordCloud(tweets, search)
            
            context = super().get_context_data(**kwargs)
            context['chartsInfo'] = charts_info
            context['wordcloud'] = word_cloud_image
            context['option'] = option
            context['term'] = search
            context['tweets'] = tweets
            context['probability'] = round(probability, 2)
            context['amoutTweets'] = number_of_tweets

            return render(request, self.template_name, context)

class ChartData(APIView):

    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None, userid=None, term=None):
        api = ViewTweetsView.return_api_data()
    
        '''   
        api_chart = {"term": api['term'], "amoutTweets": api['amoutTweets'], 
                           "chartsInfo": api['chartsInfo']}
        '''
        #retorna o dicionario de dados para gerar os graficos com o chartjs
        #os dados da variavel global foram obtidos anteriormente com as funções "generate_simple_data" e "generate_advanced_data"
        
        return Response(api)