from django.views.generic import TemplateView
from django.shortcuts import render
from django.contrib import messages
from rest_framework.views import APIView
from rest_framework.response import Response

from myLibs.data_processing import create_dict
from myLibs.chart_generator import create_chart, create_chart_training
from myLibs.training import create_dict_training
from myLibs.word_cloud import wordCloud


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
                
                # if para veficiar se o usuario fez alguma pesquisa
                if search:      
                    consumerKey = self.request.user.consumerKey
                    consumerSecret = self.request.user.consumerSecret
                    accessToken = self.request.user.accessToken
                    accessTokenSecret = self.request.user.accessTokenSecret
                    bearerToken = self.request.user.bearerToken

                    option = request.POST['inlineRadioOptions']
                    
                    print(option)
                    
                    #Verifica a opção escolhida e salva as funções que tratam os respectivos tipos de escolha em uma variavel
                    if option == 'simples':
                        search_type = create_dict
                        chart_type = create_chart

                    elif option == 'treinamento':
                        search_type = create_dict_training
                        chart_type = create_chart_training
                    
                    tweets = search_type(search, amoutTweets, consumerKey, consumerSecret, 
                                            accessToken, accessTokenSecret, bearerToken)
                    
                    chartsInfo = chart_type(tweets, search, pie=True, bar=True)
                    
                    api = {"term": search, "amoutTweets": amoutTweets, 
                           "chartsInfo": chartsInfo, "tweets": tweets,}
                    
                    uri = wordCloud(tweets, search)
    
                    context = super().get_context_data(**kwargs)
                    context['wordcloud'] = uri
                    context['option'] = option
                    context['term'] = search
                    context['tweets'] = tweets
                    context['amoutTweets'] = amoutTweets
                    context['tweetsAnalyzed'] = len(tweets)
                    context['tweetsError'] = int(amoutTweets) - len(tweets)
                    context['qtd_tweets'] = chartsInfo['qtd_tweets']
                    return render(request, 'tweets/viewtweets.html', context)
                
                # else para se o usuario não fez alguma pesquisa
                else:       
                    messages.success(request, 'Você deve pesquisar algo')
                    return render(request, 'tweets/searchtweets.html')
        

class ChartData(APIView):

    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        api = get_api()
        
        #retorna o dicionario de dados para gerar os graficos com o chartjs
        #os dados da variavel global foram obtidos anteriormente com as funções "create_chart" e "create_chart_training"
        
        return Response(api)  
    
def get_api():
    global api
    return api