import snscrape.modules.twitter as sntwitter

from my_libs.data_processing import clean_tweet
from my_libs.training_analysis import analyze_tweet, inicialize


'''
Coleta tweets utilizando Web Scraping. Não é necessario cadastro.
'''


def search_tweets_scraper(options):
    tweets = []
    
    classificador = inicialize(options['type_of_analysis'])
    
    for tweet in sntwitter.TwitterSearchScraper(options['search']).get_items():
        if len(tweets) == options['number_of_tweets']:
            break
        else:
            tweet_dict = {}
            tweet_dict['tweet_text'] = tweet.content
            tweet_dict['tweet_created_at'] = tweet.date
            tweet_dict['username'] = tweet.user.username
            tweet_dict['tweet_lang'] = tweet.lang
            tweet_dict['tweet_id'] = tweet.id
            tweet_dict['tweet_clean'] = clean_tweet(tweet_dict['tweet_text'])
            tweet_dict['tweet_analise'] = analyze_tweet(tweet_dict['tweet_clean'], classificador)
            tweets.append(tweet_dict)
    
    return tweets