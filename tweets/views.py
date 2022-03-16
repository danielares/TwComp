from django.views.generic import TemplateView
from django.shortcuts import render
from django.contrib import messages
from django.http import JsonResponse


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

                    if option == 'completa':
                        tweets = create_dict(search, amoutTweets, consumerKey, consumerSecret, 
                                            accessToken, accessTokenSecret, bearerToken)
                        tweets_human_training = create_dict_training(search, amoutTweets, consumerKey, consumerSecret, 
                                                                    accessToken, accessTokenSecret, bearerToken)
                        
                        qtd_tweets_polarity = create_chart(tweets, search)
                        qtd_tweets_polarity_training = create_chart_training(tweets_human_training, search)
                        
                        context = super().get_context_data(**kwargs)
                        context['term'] = search
                        context['tweets'] = tweets
                        context['tweets_human_training'] = tweets_human_training
                        context['amoutTweets'] = amoutTweets
                        context['tweetsAnalyzed'] = len(tweets)
                        context['tweetsError'] = int(amoutTweets) - len(tweets)
                        context['qtd_tweets_polarity'] = qtd_tweets_polarity
                        context['qtd_tweets_polarity_training'] = qtd_tweets_polarity_training
                        return render(request, 'tweets/viewtweets.html', context)
                    
                    elif option == 'traducao':
                        tweets = create_dict(search, amoutTweets, consumerKey, consumerSecret, 
                                            accessToken, accessTokenSecret, bearerToken)
                        qtd_tweets_polarity = create_chart(tweets, search)
                        context = super().get_context_data(**kwargs)
                        context['term'] = search
                        context['tweets'] = tweets
                        context['amoutTweets'] = amoutTweets
                        context['tweetsAnalyzed'] = len(tweets)
                        context['tweetsError'] = int(amoutTweets) - len(tweets)
                        context['qtd_tweets_polarity'] = qtd_tweets_polarity
                        return render(request, 'tweets/viewtweets.html', context)
                    
                    else:
                        
                        tweets_human_training = create_dict_training(search, amoutTweets, consumerKey, consumerSecret, 
                                                                    accessToken, accessTokenSecret, bearerToken)
                        qtd_tweets_polarity_training = create_chart_training(tweets_human_training, search)
                        wordCloud(tweets_human_training)
                        
                        #create_chart(tweets, search)
                        context = super().get_context_data(**kwargs)
                        context['term'] = search
                        context['tweets_human_training'] = tweets_human_training
                        context['amoutTweets'] = amoutTweets
                        context['tweetsAnalyzed'] = len(tweets_human_training)
                        context['tweetsError'] = int(amoutTweets) - len(tweets_human_training)
                        context['qtd_tweets_polarity_training'] = qtd_tweets_polarity_training
                        return render(request, 'tweets/viewtweets.html', context)
                
                # else para se o usuario não fez alguma pesquisa
                else:       
                    messages.success(request, 'Você deve pesquisar algo')
                    return render(request, 'tweets/searchtweets.html')
        