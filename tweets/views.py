from multiprocessing import get_context
from django.views.generic import TemplateView
from django.shortcuts import render
from django.contrib import messages

from .data_processing import searchTweets
from .chart_generator import count_polarity


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
            if request.method == 'POST':
                
                search = request.POST['searched']
                amoutTweets = request.POST['amoutTweets']
                
                
                if search:      # if para veficiar se o usuario fez alguma pesquisa
                    consumerKey = self.request.user.consumerKey
                    consumerSecret = self.request.user.consumerSecret
                    accessToken = self.request.user.accessToken
                    accessTokenSecret = self.request.user.accessTokenSecret
                    bearerToken = self.request.user.bearerToken
                
                    tweets = searchTweets(search, amoutTweets, consumerKey, consumerSecret, accessToken, accessTokenSecret, bearerToken)
                    count_polarity(tweets, search)
                    
                    context = super().get_context_data(**kwargs)
                    context['term'] = search
                    context['tweets'] = tweets
                    
                    return render(request, 'tweets/viewtweets.html', context)
                
                else:       # else para se o usuario não fize alguma pesquisa
                    messages.success(request, 'Você deve pesquisar algo')
                    return render(request, 'tweets/searchtweets.html')
        