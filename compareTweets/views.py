from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib import messages
from rest_framework.views import APIView
from rest_framework.response import Response

from myLibs.word_cloud import wordCloud
from myLibs.return_data_view import get_tweets


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
                     
                    bearerToken = self.request.user.bearerToken 
                    
                    tweets1, chartsInfo1 = get_tweets(search1, amoutTweets, option, bearerToken)
                    tweets2, chartsInfo2 = get_tweets(search2, amoutTweets, option, bearerToken)
                    
                    wordcloud1 = wordCloud(tweets1, search1)
                    wordcloud2 = wordCloud(tweets2, search2)
                    
                    api = {"term1": search1, "term2": search2, 
                            "amoutTweets": amoutTweets, 
                            "chartsInfo1": chartsInfo1, "chartsInfo2": chartsInfo2,
                            "tweets1": tweets1, "tweets2": tweets2}

                    context = super().get_context_data(**kwargs)
                    context['chartsInfo1'] = chartsInfo1
                    context['chartsInfo2'] = chartsInfo2
                    context['wordcloud1'] = wordcloud1
                    context['wordcloud2'] = wordcloud2
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
                
        @staticmethod
        def return_api_data():
            global api
            return api
        
        
class CompareChartData(APIView):
    authentication_classes = []
    permission_classes = []
    def get(self, request, format=None):
        api = CompareTweetsView.return_api_data()
        
        api_chart = {"term1": api['term1'], "term2": api['term2'],
                     "amoutTweets": api['amoutTweets'], 
                     "chartsInfo1": api['chartsInfo1'],
                     "chartsInfo2": api['chartsInfo2'],}
        
        #retorna o dicionario de dados para gerar os graficos com o chartjs
        #os dados da variavel global foram obtidos anteriormente com as funções "generate_simple_data" e "generate_advanced_data"
        return Response(api_chart)