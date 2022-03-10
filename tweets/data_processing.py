import re
import tweepy
from textblob import TextBlob
from googletrans import Translator

def getClient(consumerKey, consumerSecret, accessToken, accessTokenSecret, bearerToken):
    client = tweepy.Client(consumer_key=consumerKey,
                           consumer_secret=consumerSecret,
                           access_token=accessToken,
                           access_token_secret=accessTokenSecret,
                           bearer_token=bearerToken)
    return client


def searchTweets(query, amount, consumerKey, consumerSecret, accessToken, accessTokenSecret, bearerToken):
    client = getClient(consumerKey, consumerSecret, accessToken, accessTokenSecret, bearerToken)
    tweets = client.search_recent_tweets(query=query, max_results=amount)
    tweet_data = tweets.data
    
    results = []

    if not tweet_data is None and len(tweet_data) > 0:
        for tweet in tweet_data:
            
            ''' Filter to exclude retweets
            if tweet.text[:2] != "RT":
                tweet_dict = {}
                tweet_dict['id'] = tweet.id
                tweet_dict['text'] = tweet.text
                results.append(tweet_dict),
            '''
            tweet_dict = {}
            tweet_dict['id'] = tweet.id
            tweet_dict['text'] = tweet.text
            
            results.append(tweet_dict)

    return create_dict(results)


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


def translator(tweet):
    try:
        translator = Translator()
        tweet_english = translator.translate(tweet, dest='en')
        return tweet_english
    except:
        return 'erro ao traduzir'


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
        
        
def create_dict(data):
    tweets = []
    tweets_dict = {}
    for tweet in data:
        try:
            tweet_id = tweet['id']
            tweet_text = tweet['text']
            tweet_clean = clean_tweet(tweet_text)
            tweet_english = translator(tweet_clean)
            sentimento = analise_sentimento(tweet_english.text)
            polaridade = get_polarity(sentimento)
            
            tweets_dict = {
                'tweet_id': tweet_id,
                'tweet_text': tweet_text,
                'tweet_clean': tweet_clean,
                'tweet_english': tweet_english,
                'sentimento': sentimento,
                'polaridade': polaridade,
            }
            
            tweets.append(tweets_dict)
        except:
            print('deu erro')   
    
    return tweets


