from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib import messages

from myLibs.data_processing import create_dict
from myLibs.chart_generator import create_chart, create_chart_training
from myLibs.training import create_dict_training


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
        if request.method == 'POST':
            search1 = request.POST['searched1']
            search2 = request.POST['searched2']
            amoutTweets = request.POST['amoutTweets']
            option = request.POST['inlineRadioOptions']
            
            if search1 and search2:
                '''
                tweets = create_dict(search1, 
                                    amoutTweets, 
                                    self.request.user.consumerKey, 
                                    self.request.user.consumerSecret, 
                                    self.request.user.accessToken, 
                                    self.request.user.accessTokenSecret, 
                                    self.request.user.bearerToken)
                
                tweets = create_dict(search2, 
                                    amoutTweets, 
                                    self.request.user.consumerKey, 
                                    self.request.user.consumerSecret, 
                                    self.request.user.accessToken, 
                                    self.request.user.accessTokenSecret, 
                                    self.request.user.bearerToken)
                '''
                
                tweets_human_training1 = create_dict_training(search1, 
                                                            amoutTweets, 
                                                            self.request.user.consumerKey, 
                                                            self.request.user.consumerSecret, 
                                                            self.request.user.accessToken, 
                                                            self.request.user.accessTokenSecret, 
                                                            self.request.user.bearerToken)
                
                tweets_human_training2 = create_dict_training(search2, 
                                                            amoutTweets, 
                                                            self.request.user.consumerKey, 
                                                            self.request.user.consumerSecret, 
                                                            self.request.user.accessToken, 
                                                            self.request.user.accessTokenSecret, 
                                                            self.request.user.bearerToken)
                
                #qtd_tweets_polarity = create_chart(tweets, search1)
                #qtd_tweets_polarity = create_chart(tweets, search2)
                qtd_tweets_polarity_training1 = create_chart_training(tweets_human_training1, search1)
                qtd_tweets_polarity_training2 = create_chart_training(tweets_human_training2, search2)
                
                context = super().get_context_data(**kwargs)
                context['term1'] = search1
                context['term2'] = search2
                #context['tweets'] = tweets
                context['tweets_human_training1'] = tweets_human_training1
                context['tweets_human_training2'] = tweets_human_training2
                context['amoutTweets'] = amoutTweets
                #context['tweetsAnalyzed'] = len(tweets)
                #context['tweetsError'] = int(amoutTweets) - len(tweets)
                #context['qtd_tweets_polarity'] = qtd_tweets_polarity
                context['qtd_tweets_polarity_training1'] = qtd_tweets_polarity_training1
                context['qtd_tweets_polarity_training2'] = qtd_tweets_polarity_training2
                
                return render(request, 'compareTweets/view-compare-tweets.html', context)
            
            else:       
                messages.success(request, 'Você deve pesquisar algo')
                return render(request, 'compareTweets/compare-tweets.html')