from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib import messages
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.utils.datastructures import MultiValueDictKeyError

from my_libs.word_cloud import wordCloud
from my_libs.return_data_view import get_tweets


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
            
            search_1 = request.POST['searched1']
            search_2 = request.POST['searched2']
            number_of_tweets = request.POST['amoutTweets']
            option = request.POST['inlineRadioOptions']
            
            try:
                filter_retweets = bool(request.POST['filterRetweets'])
            except MultiValueDictKeyError:
                filter_retweets = False
            
            try:
                filter_reply = bool(request.POST['filterReply'])
            except MultiValueDictKeyError:
                filter_reply = False
            
            # if para veficiar se o usuario fez alguma pesquisa
            if search_1 and search_2:
                    
                tokens = self.request.user.bearerToken 
                
                tweets1, chartsInfo1 = get_tweets(search_1, number_of_tweets, option, filter_retweets, filter_reply, tokens)
                tweets2, chartsInfo2 = get_tweets(search_2, number_of_tweets, option, filter_retweets, filter_reply, tokens)
                
                wordcloud_image_1 = wordCloud(tweets1, search_1)
                wordcloud_image_2 = wordCloud(tweets2, search_2)
                
                
                api = {"term1": search_1, "term2": search_2,
                        "amoutTweets": number_of_tweets,
                        "chartsInfo1": chartsInfo1, "chartsInfo2": chartsInfo2,
                        "tweets1": tweets1, "tweets2": tweets2}

                context = super().get_context_data(**kwargs)
                context['chartsInfo1'] = chartsInfo1
                context['chartsInfo2'] = chartsInfo2
                context['wordcloud1'] = wordcloud_image_1
                context['wordcloud2'] = wordcloud_image_2
                context['option'] = option
                context['amoutTweets'] = number_of_tweets
                context['term1'] = search_1
                context['term2'] = search_2
                context['tweets1'] = tweets1
                context['tweets2'] = tweets2
                context['qtd_tweets1'] = chartsInfo1['qtd_tweets']
                context['qtd_tweets2'] = chartsInfo2['qtd_tweets']    
            
                return render(request, self.template_name, context)
            
            # else para se o usuario não fez alguma pesquisa
            else:       
                messages.success(request, 'Você deve pesquisar algo')
                return redirect('search-tweets-compare')
                
        @staticmethod
        def return_api_data():
            global api
            return api
        
        
class CompareChartData(APIView):
    authentication_classes = []
    permission_classes = []
    def get(self, request, format=None, userid=None, term1=None, term2=None):
        api = CompareTweetsView.return_api_data()
        '''
        api_chart = {"term1": api['term1'], "term2": api['term2'],
                     "amoutTweets": api['amoutTweets'], 
                     "chartsInfo1": api['chartsInfo1'],
                     "chartsInfo2": api['chartsInfo2'],}
        '''
        #retorna o dicionario de dados para gerar os graficos com o chartjs
        #os dados da variavel global foram obtidos anteriormente com as funções "generate_simple_data" e "generate_advanced_data"
        return Response(api)