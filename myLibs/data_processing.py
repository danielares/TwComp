import re
import tweepy
from itertools import zip_longest


def getClient(consumerKey, consumerSecret, accessToken, accessTokenSecret, bearerToken):
    client = tweepy.Client(consumer_key=consumerKey,
                           consumer_secret=consumerSecret,
                           access_token=accessToken,
                           access_token_secret=accessTokenSecret,
                           bearer_token=bearerToken)
    return client


def searchTweets(query, amount, consumerKey, consumerSecret, accessToken, accessTokenSecret, bearerToken):
    client = getClient(consumerKey, consumerSecret, accessToken, accessTokenSecret, bearerToken)
    
    expansions_options = ['author_id','referenced_tweets.id']
    tweet_fields_options = ['created_at','lang','geo','text', 'referenced_tweets']
    
    tweets = client.search_recent_tweets(query=query, max_results=amount, expansions=expansions_options, 
                                         tweet_fields=tweet_fields_options)
    
    tweet_data = tweets.data
    tweets_users = tweets.includes['users']
    
    results = []

    if not tweet_data is None and len(tweet_data) > 0:
        try:
            for (tweet, tweet_user) in zip_longest(tweet_data, tweets_users):
                tweet_dict = {}
                tweet_dict['username'] = tweet_user.username
                tweet_dict['id'] = tweet.id
                if tweet.text[:2] != "RT":
                    tweet_dict['text'] = tweet.text
                else:
                    # USADO PQ A API DO TWITTER NÃO ENTREGA OS RETWEETS POR COMPLETO NO TWEET.TEXT DO IF ACIMA
                    # O RETWEET COMPLETO ESTA LOCALIZADO NO TWEETS.INCLUDES
                    # COM ESSA CONDIÇÃO É POSSIVEL PEGAR O RETWEET COMPLETO E SALVA-LO NO DICIONARIO
                    
                    id_retweet_no_tweet_original = tweet['referenced_tweets']
                    id = id_retweet_no_tweet_original[0].id
                    
                    for retweet in tweets.includes['tweets']:
                        id_retweet = retweet.id
                        if id == id_retweet:
                            tweet_dict['text'] = retweet.text

                tweet_dict['created_at'] = tweet.created_at
                tweet_dict['lang'] = tweet.lang
                tweet_dict['geo'] = tweet.geo
                tweet_dict['referenced_tweets'] = tweet.referenced_tweets
                results.append(tweet_dict)
        except:
            print('deu erro na coleta')
            
    return results


def clean_tweet(tweet):
        tweet_clean = re.sub(r"\n", " ", tweet)
        tweet_clean = re.sub(
        "[^0-9A-Za-z ñÑÀàÁáÉéÍíÓóÚúÂâÊêÎîÔôÛûÃãÕõÇç@#']", "", tweet_clean).lower()  # deixa somente os caracteres aceitos
        tweet_clean = re.sub(r"http\S+", "", tweet_clean)  # remove links
        tweet_clean = re.sub(r"@\S+", "", tweet_clean)  # remove @USERNAME
        tweet_clean = re.sub(r"#\S+", "", tweet_clean)  # remove hashtags
        tweet_clean = re.sub(r"ñ", "não", tweet_clean)  # substitui ñ por não
        tweet_clean = re.sub(r"^B\S([rt]+)?", "", tweet_clean)  # remover rt do inicio dos retweets
        tweet_clean = tweet_clean.strip()
        return tweet_clean