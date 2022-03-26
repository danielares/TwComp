from django.views.generic import TemplateView
from django.shortcuts import render
from django.contrib import messages
from rest_framework.views import APIView
from rest_framework.response import Response

from myLibs.word_cloud import wordCloud
from myLibs.return_data_view import get_tweets


class TakeTweetsView(TemplateView):
    template_name = 'tweets/searchtweets.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #context = {"term": "pesquisa_termo"} FUNCIONOU
        return context


class TakeTweetsView(TemplateView):
    template_name = 'tweets/searchtweets.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    

class ViewTweetsView(TemplateView):
        template_name = 'tweets/viewtweets.html'
        
        def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            return context
                
        def post(self, request, **kwargs):
            global api
            
            if request.method == 'POST':
                
                search = request.POST['searched']
                amoutTweets = request.POST['amoutTweets']
                option = request.POST['inlineRadioOptions']  
                
                # if para veficiar se o usuario fez alguma pesquisa
                if search:
                    
                    bearerToken = self.request.user.bearerToken
                    
                    tweets, chartsInfo = get_tweets(search, amoutTweets, option, bearerToken) 
                    wordCloudImage = wordCloud(tweets, search)
                    

                    api = {"term": search, "amoutTweets": amoutTweets, 
                   "chartsInfo": chartsInfo, 'tweets': tweets}
    
                    context = super().get_context_data(**kwargs)
                    context['chartsInfo'] = chartsInfo
                    context['wordcloud'] = wordCloudImage
                    context['option'] = option
                    context['term'] = search
                    context['tweets'] = tweets
                    context['amoutTweets'] = amoutTweets
                    context['tweetsAnalyzed'] = len(tweets) # FAZER ISSO DIRETAMENTE QUANDO CRIA O DICIONARIO DOS TWEETS E RETORNAR O VALOR DENTRO DO DICIONARIO
                    context['tweetsError'] = int(amoutTweets) - len(tweets) # FAZER ISSO DIRETAMENTE QUANDO CRIA O DICIONARIO DOS TWEETS E RETORNAR O VALOR DENTRO DO DICIONARIO
                    context['qtd_tweets'] = chartsInfo['qtd_tweets'] # FAZER ISSO DIRETAMENTE QUANDO CRIA O DICIONARIO DOS TWEETS E RETORNAR O VALOR DENTRO DO DICIONARIO
                    return render(request, 'tweets/viewtweets.html', context)
                
                # else para se o usuario não fez alguma pesquisa
                else:       
                    messages.success(request, 'Você deve pesquisar algo')
                    return render(request, 'tweets/searchtweets.html')
                
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

    def get(self, request, format=None):
        api = ViewTweetsView.return_api_data()
    
        api_chart = {"term": api['term'], "amoutTweets": api['amoutTweets'], 
                           "chartsInfo": api['chartsInfo']}
    
        #retorna o dicionario de dados para gerar os graficos com o chartjs
        #os dados da variavel global foram obtidos anteriormente com as funções "generate_simple_data" e "generate_advanced_data"
        
        return Response(api_chart)