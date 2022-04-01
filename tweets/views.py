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
        
            try:
                filter_retweets = bool(request.POST['filterRetweets'])
            except MultiValueDictKeyError:
                filter_retweets = False
            
            # if para veficiar se o usuario fez alguma pesquisa
            if search:
                
                tokens = self.request.user.bearerToken
                tweets, charts_info = get_tweets(search, number_of_tweets, option, filter_retweets, tokens) 
                word_cloud_image = wordCloud(tweets, search)
                api = {"term": search, "amoutTweets": number_of_tweets, 
                        "chartsInfo": charts_info, 'tweets': tweets}

                context = super().get_context_data(**kwargs)
                context['chartsInfo'] = charts_info
                context['wordcloud'] = word_cloud_image
                context['option'] = option
                context['term'] = search
                context['tweets'] = tweets
                context['amoutTweets'] = number_of_tweets
                context['tweetsAnalyzed'] = len(tweets) # FAZER ISSO DIRETAMENTE QUANDO CRIA O DICIONARIO DOS TWEETS E RETORNAR O VALOR DENTRO DO DICIONARIO
                context['tweetsError'] = int(number_of_tweets) - len(tweets) # FAZER ISSO DIRETAMENTE QUANDO CRIA O DICIONARIO DOS TWEETS E RETORNAR O VALOR DENTRO DO DICIONARIO
                context['qtd_tweets'] = charts_info['qtd_tweets'] # FAZER ISSO DIRETAMENTE QUANDO CRIA O DICIONARIO DOS TWEETS E RETORNAR O VALOR DENTRO DO DICIONARIO
                return render(request, self.template_name, context)
            # else para se o usuario não fez alguma pesquisa
            else:       
                messages.success(request, 'Você deve pesquisar algo')
                return redirect('search-tweets')
                
        @staticmethod
        def return_api_data():
            global api
            return api
        
class ViewAllTweetsView(TemplateView):
    template_name = 'tweets/view-all-tweets.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        api = ViewTweetsView.return_api_data()
        context = {"chartsInfo": api['chartsInfo'],
                   "tweets": api['tweets']}
                   
        return context


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