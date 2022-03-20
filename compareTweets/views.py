from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib import messages
from rest_framework.views import APIView
from rest_framework.response import Response

from myLibs.data_processing import create_dict
from myLibs.chart_generator import create_chart, create_chart_training
from myLibs.training import create_dict_training
from myLibs.word_cloud import wordCloud


class ViewCompareTweetsView(TemplateView):
    template_name = 'compareTweets/compare-tweets.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
             
             
class CompareTweetsView(TemplateView):
        template_name = 'compareTweets/viewtweetscompare.html'
        
        def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            return context
                
        def post(self, request, **kwargs):
            global api
            
            if request.method == 'POST':
                search1 = request.POST['searched1']
                search2 = request.POST['searched2']
                amoutTweets = request.POST['amoutTweets']
                option = request.POST['inlineRadioOptions']
                
                # if para veficiar se o usuario fez alguma pesquisa
                if search1 and search2:
                     
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
                    
                    #PESQUISAS RELACIONADAS AO PRIMEIRO TERMO
                    tweets1 = search_type(search1, amoutTweets, consumerKey, consumerSecret, 
                                            accessToken, accessTokenSecret, bearerToken)
                    
                    chartsInfo1 = chart_type(tweets1, search1)
                    
                    #PESQUISAS RELACIONADAS AO SEGUNDO TERMO
                    tweets2 = search_type(search2, amoutTweets, consumerKey, consumerSecret, 
                        accessToken, accessTokenSecret, bearerToken)
                    chartsInfo2 = chart_type(tweets2, search2)
                    
                    api = {"term1": search1, "term2": search2, 
                            "amoutTweets": amoutTweets, 
                           "chartsInfo1": chartsInfo1, "chartsInfo2": chartsInfo2,
                           "tweets1": tweets1, "tweets2": tweets2}
                    
                    wordCloud(tweets1, search1)
                    wordCloud(tweets2, search2)

                    context = super().get_context_data(**kwargs)
                    context['option'] = option
                    context['amoutTweets'] = amoutTweets
                    context['term1'] = search1
                    context['term2'] = search2
                    context['tweets1'] = tweets1
                    context['tweets2'] = tweets2
                    context['qtd_tweets1'] = chartsInfo1['qtd_tweets']
                    context['qtd_tweets2'] = chartsInfo2['qtd_tweets']
                
                    return render(request, 'compareTweets/view-compare-tweets.html', context)
                
                # else para se o usuario não fez alguma pesquisa
                else:       
                    messages.success(request, 'Você deve pesquisar algo')
                    return render(request, 'tweets/searchtweets.html')


class CompareChartData(APIView):
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