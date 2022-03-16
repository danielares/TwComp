import re
import tweepy
from textblob import TextBlob
from googletrans import Translator
from itertools import zip_longest

import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
STOPWORDS = set(stopwords.words('english'))
from nltk.tokenize import word_tokenize
from nltk.tokenize.treebank import TreebankWordDetokenizer

def getClient(consumerKey, consumerSecret, accessToken, accessTokenSecret, bearerToken):
    client = tweepy.Client(consumer_key=consumerKey,
                           consumer_secret=consumerSecret,
                           access_token=accessToken,
                           access_token_secret=accessTokenSecret,
                           bearer_token=bearerToken)
    return client


def retweetTake(id):
    client = getClient()
    retweet = client.get_tweet(id)
    text_retweet = retweet.data['text']
    return text_retweet


def searchTweets(query, amount, consumerKey, consumerSecret, accessToken, accessTokenSecret, bearerToken):
    client = getClient(consumerKey, consumerSecret, accessToken, accessTokenSecret, bearerToken)
    
    expansions_options = ['author_id','referenced_tweets.id']
    tweet_fields_options = ['created_at','lang','geo','text', 'referenced_tweets']
    
    tweets = client.search_recent_tweets(query=query, max_results=amount, expansions=expansions_options, 
                                         tweet_fields=tweet_fields_options)
    
    tweet_data = tweets.data
    tweets_users = tweets.includes['users']
    tweets_rt = tweets.includes['tweets']
    
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
                    #retweet = retweetTake(tweet.referenced_tweets[0]['id'])
                    tweet_dict['text'] = tweet.text
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
        tweet_clean = re.sub(r"Ñ", "não", tweet_clean)  # substitui Ñ por não
        tweet_clean = re.sub(r"ñ", "não", tweet_clean)  # substitui ñ por não
        tweet_clean = tweet_clean.strip()
        return tweet_clean


def translatorGoogle(tweet):
    try:
        translator = Translator()
        tweet_english = translator.translate(tweet, dest='en')
        return tweet_english
    except:
        return 'erro ao traduzir'

def translatorTextBlob(tweet):
    try:
        tweet_english = TextBlob(tweet)
        tweet_english = tweet_english.translate(to='en')
        return str(tweet_english)
    except:
        return 'erro ao traduzir'
    

def remove_stopwords(tweet):
    tweet_without_stopwords = TextBlob(tweet)
    tokens = word_tokenize(str(tweet_without_stopwords))
    tweet_without_stopwords = [word for word in tokens if not word in STOPWORDS]
    tweet_without_stopwords = TreebankWordDetokenizer().detokenize(tweet_without_stopwords)
    return tweet_without_stopwords

def analise_sentimento(tweet):
    tweet_text = TextBlob(tweet)
    sentimento = tweet_text.sentiment
    return sentimento


def get_polarity(polarity):
    if polarity.polarity < 0:
        return 'negative'
    elif polarity.polarity == 0:
        return 'neutral'
    else:
        return 'positive'
        
        
def create_dict(query, amount, consumerKey, consumerSecret, accessToken, accessTokenSecret, bearerToken):
    tweets = []
    tweets_dict = {}
    
    data = searchTweets(query, amount, consumerKey, consumerSecret, accessToken, accessTokenSecret, bearerToken)
    
    for tweet in data:
        try:
            tweet_id = tweet['id']
            tweet_text = tweet['text']
            
            tweet_created_at = tweet['created_at']
            tweet_lang = tweet['lang']
            tweet_geo = tweet['geo']
            tweet_referenced_tweets = tweet['referenced_tweets']
            tweet_username = tweet['username']
            
            tweet_clean = clean_tweet(tweet_text)
            tweet_english = translatorTextBlob(tweet_clean)
            tweet_without_stopwords = remove_stopwords(tweet_english)
            sentimento = analise_sentimento(tweet_without_stopwords)
            polaridade = get_polarity(sentimento)
            
            tweets_dict = {
                'tweet_id': tweet_id,
                'tweet_text': tweet_text,
                                
                'tweet_created_at': tweet_created_at,
                'tweet_lang': tweet_lang,
                'tweet_geo': tweet_geo,
                'tweet_referenced_tweets': tweet_referenced_tweets,
                'tweet_username': tweet_username,
                                
                'tweet_clean': tweet_clean,
                'tweet_english': tweet_english,
                'tweet_without_stopwords': tweet_without_stopwords,
                'sentimento': sentimento,
                'polaridade': polaridade,
            }
            
            tweets.append(tweets_dict)
        except:
            print('deu erro')   
    
    return tweets

