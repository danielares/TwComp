from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib import messages
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.utils.datastructures import MultiValueDictKeyError

import json

from my_libs.word_cloud import wordCloud
from my_libs.return_data_view import get_tweets
from my_libs.training_analysis import search_tweets_scraper
from my_libs.return_data_view import generate_data, probability_average

@method_decorator(login_required, name='dispatch')
class ViewCompareTweetsView(TemplateView):
    template_name = 'compareTweets/search-tweets-compare.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
  

class CompareTweetsView(TemplateView):
        template_name = 'compareTweets/view-tweets-compare.html'
        
        def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            return context
                
        def post(self, request, **kwargs):
            global api         
            
            options1 = {}
            options2 = {}
            
            options1['search'] = request.POST['searched1']
            options2['search'] = request.POST['searched2']
            
            options1['number_of_tweets'] = request.POST['amoutTweets']
            options2['number_of_tweets'] = request.POST['amoutTweets']
            
            options1['type_of_analysis'] = request.POST['inlineRadioOptions']
            options2['type_of_analysis'] = request.POST['inlineRadioOptions']
            
            # Opção para incluir mapas
            try: 
                options1['option_maps'] = request.POST['includeMaps']
                options2['option_maps'] = request.POST['includeMaps']
            except: 
                 options1['option_maps'] = False
                 options2['option_maps'] = False
            
            # Opção para filtrar retweets
            try: 
                options1['filter_retweets'] = bool(request.POST['filterRetweets'])
                options2['filter_retweets'] = bool(request.POST['filterRetweets'])
            except MultiValueDictKeyError: 
                options1['filter_retweets'] = False
                options2['filter_retweets'] = False
            
            # Opção para filtrar respostas
            try: 
                options1['filter_reply'] = bool(request.POST['filterReply'])
                options2['filter_reply'] = bool(request.POST['filterReply'])
            except MultiValueDictKeyError: 
                options1['filter_reply'] = False
                options2['filter_reply'] = False
            
            # if para veficiar se o usuario fez alguma pesquisa
            if not options1['search'] or not options2['search']:
                messages.error(request, 'Você deve digitar dois termos para pesquisar')
                return redirect('search-tweets-compare')
                    
            api_access_tokens = self.request.user.bearerToken 
            
            tweets1, chartsInfo1, probability1, geo_locations1, context_infos = get_tweets(api_access_tokens, options1)
            tweets2, chartsInfo2, probability2, geo_locations2, context_infos = get_tweets(api_access_tokens, options2)
            probability = round((probability1 + probability2)/2, 2)

            wordcloud_image_1 = wordCloud(tweets1, options1['search'])
            wordcloud_image_2 = wordCloud(tweets2, options2['search'])
            
            
            request.session['search1'] = options1['search']
            request.session['number_of_tweets1'] = options1['number_of_tweets']
            request.session['charts_info1'] = chartsInfo1
            request.session['tweets1'] = json.dumps(tweets1, indent=4, sort_keys=True, default=str)
            
            request.session['search2'] = options2['search']
            request.session['number_of_tweets2'] = options2['number_of_tweets']
            request.session['charts_info2'] = chartsInfo2
            request.session['tweets2'] = json.dumps(tweets2, indent=4, sort_keys=True, default=str)

            context = super().get_context_data(**kwargs)
            context['chartsInfo1'] = chartsInfo1
            context['chartsInfo2'] = chartsInfo2
            context['wordcloud1'] = wordcloud_image_1
            context['wordcloud2'] = wordcloud_image_2
            context['option'] = options1['type_of_analysis']
            context['amoutTweets'] = options1['number_of_tweets']
            context['term1'] = options1['search']
            context['term2'] = options2['search']
            context['tweets1'] = tweets1
            context['tweets2'] = tweets2
            context['probability'] = probability
            context['qtd_tweets1'] = chartsInfo1['qtd_tweets']
            context['qtd_tweets2'] = chartsInfo2['qtd_tweets']
            context['locations1'] = geo_locations1
            context['locations2'] = geo_locations2
        
            return render(request, self.template_name, context)
                
        @staticmethod
        def return_api_data():
            global api
            return api
        
        
class ScraperTweetsCompareView(TemplateView):
        template_name = 'webscraper/search-tweets-compare-scraper.html'
        
        def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            return context    
        
        
class ViewScraperTweetsCompareView(TemplateView):
    template_name = 'webscraper/view-tweets-compare-scraper.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def post(self, request, **kwargs):
        options1 = {}
        options2 = {}
        
        options1['search'] = request.POST['searched1']
        options2['search'] = request.POST['searched2']
        options1['number_of_tweets'] = int(request.POST['amoutTweets'])
        options2['number_of_tweets'] = int(request.POST['amoutTweets'])
        options1['type_of_analysis'] = request.POST['inlineRadioOptions']
        options2['type_of_analysis'] = request.POST['inlineRadioOptions']
        
        if not options1['search'] or not options2['search']:
            messages.error(request, 'Você deve digitar dois termos para pesquisar')
            return redirect('search-tweets-compare-scraper')
        
        #TERMO 1
        tweets1 = search_tweets_scraper(options1)
        charts_info1 = generate_data(tweets1, options1['type_of_analysis'])
        probability1 = probability_average(tweets1)
        word_cloud_image1 = wordCloud(tweets1, options1['search'])
        
        #TERMO 2
        tweets2 = search_tweets_scraper(options2)
        charts_info2 = generate_data(tweets2, options2['type_of_analysis'])
        probability2 = probability_average(tweets2)
        word_cloud_image2 = wordCloud(tweets2, options2['search'])
        
        probability = round((probability1 + probability2)/2, 2)
        
        context = super().get_context_data(**kwargs)
        context['option'] = options1['type_of_analysis']
        context['probability'] = probability
        context['amoutTweets'] = options1['number_of_tweets']
        
        # TERMO 1:
        context['chartsInfo1'] = charts_info1
        context['wordcloud1'] = word_cloud_image1
        context['term1'] = options1['search']
        context['tweets1'] = tweets1
        
        # TERMO 2:
        context['chartsInfo2'] = charts_info2
        context['wordcloud2'] = word_cloud_image2
        context['term2'] = options2['search']
        context['tweets2'] = tweets2

        return render(request, self.template_name, context)