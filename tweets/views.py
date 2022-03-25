from django.views.generic import TemplateView
from django.shortcuts import render
from django.contrib import messages
from rest_framework.views import APIView
from rest_framework.response import Response

from myLibs.generate_api_data import generate_simple_data, generate_advanced_data
from myLibs.training_analysis import create_dict_training
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
                option = request.POST['inlineRadioOptions']  
                
                # if para veficiar se o usuario fez alguma pesquisa
                if search:
                    
                    consumerKey = self.request.user.consumerKey
                    consumerSecret = self.request.user.consumerSecret
                    accessToken = self.request.user.accessToken
                    accessTokenSecret = self.request.user.accessTokenSecret
                    bearerToken = self.request.user.bearerToken
                    
                    tweets, chartsInfo = self.get_tweets(search, amoutTweets, option, 
                                                         consumerKey, consumerSecret, accessToken, accessTokenSecret, bearerToken)
                    
                    
                    wordCloudImage = wordCloud(tweets, search)
    
                    context = super().get_context_data(**kwargs)
                    context['wordcloud'] = wordCloudImage
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
                
                
        def get_tweets(search, amoutTweets, option, 
                       consumerKey, consumerSecret, accessToken, accessTokenSecret, bearerToken):
            
            # Verifica a opção de analise de tweets escolhida
            if option == 'simple': chart_type = generate_simple_data
            elif option == 'advanced': chart_type = generate_advanced_data

            tweets = create_dict_training(option, search, amoutTweets, consumerKey, consumerSecret, 
                                          accessToken, accessTokenSecret, bearerToken)

            chartsInfo = chart_type(tweets)

            api = {"term": search, "amoutTweets": amoutTweets, 
                   "chartsInfo": chartsInfo, 'tweets': tweets}

            return tweets, chartsInfo

class ChartData(APIView):

    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        api = get_api()
        
        api_chart = {"term": api['term'], "amoutTweets": api['amoutTweets'], 
                           "chartsInfo": api['chartsInfo']}
        #retorna o dicionario de dados para gerar os graficos com o chartjs
        #os dados da variavel global foram obtidos anteriormente com as funções "generate_simple_data" e "generate_advanced_data"
        
        return Response(api_chart)  
    
def get_api():
    global api
    return api
