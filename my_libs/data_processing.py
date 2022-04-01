import re
import tweepy
from itertools import zip_longest


# Faz a autenticação utilizando o brarer token com o twitter atraves da biblioteca tweepy
def get_client(tokens):
    client = tweepy.Client(bearer_token=tokens)
    return client


# Procura os tweets com base no termo pesquisado
def search_tweets(search_term, number_of_tweets, filter_retweets, tokens):
    
    # chama a função que cria o cliente com o qual fazemos as requisições a API do twitter
    client = get_client(tokens)
    
    # Campos de extensão opcionais que buscados durante uma requisição na API do twitter
    expansions_options = ['author_id','referenced_tweets.id']
    tweet_fields_options = ['created_at','lang','geo','text', 'referenced_tweets']
    
    # Busca os tweets mais recentes
    # Filtro para não pegar retweets: query=search_term + ' -is:retweet
    if filter_retweets: search_term = search_term + ' -is:retweet'     
    tweets = client.search_recent_tweets(query=search_term+' lang:pt', max_results=number_of_tweets, expansions=expansions_options, 
                                         tweet_fields=tweet_fields_options)
    
    results = []

    try:
        for (tweet, tweet_user) in zip_longest(tweets.data, tweets.includes['users']):
            tweet_dict = {}
            tweet_dict['username'] = tweet_user.username
            tweet_dict['id'] = tweet.id
            if tweet.text[:2] != "RT":
                tweet_dict['text'] = tweet.text
            else:
                '''
                usado pq a api do twitter não entrega os retweets por completo no tweet.text do if acima
                o retweet completo esta localizado no tweets.includes
                com essa condição é possivel pegar o retweet completo e salva-lo no dicionario
                '''
                id_retweet = tweet['referenced_tweets']
                id_retweet = id_retweet[0].id
                
                for retweet in tweets.includes['tweets']:
                    if id_retweet == retweet.id:
                        tweet_dict['text'] = retweet.text

            tweet_dict['created_at'] = tweet.created_at
            tweet_dict['lang'] = tweet.lang
            tweet_dict['geo'] = tweet.geo
            tweet_dict['referenced_tweets'] = tweet.referenced_tweets
            results.append(tweet_dict)
    except:
        print('deu erro na coleta')
            
    return results


'''
Função para limpar os tweets 
Remove coisas que não são interessantes para a analise
Ou que atrapalham a analise
'''
def clean_tweet(tweet):
        tweet_clean = re.sub(r"\n", " ", tweet) # troca quebra de linha por um espaço em branco
        tweet_clean = re.sub(
        "[^0-9A-Za-z ñÑÀàÁáÉéÍíÓóÚúÂâÊêÎîÔôÛûÃãÕõÇç@']", "", tweet_clean).lower()  # deixa somente os caracteres aceitos
        tweet_clean = re.sub(r"http\S+", "", tweet_clean)  # remove links
        tweet_clean = re.sub(r"@\S+", "", tweet_clean)  # remove @USERNAME
        #tweet_clean = re.sub(r"#\S+", "", tweet_clean)  # remove hashtags
        tweet_clean = re.sub(r"ñ", "não", tweet_clean)  # substitui ñ por não
        tweet_clean = re.sub(r"^B\S([rt]+)?", "", tweet_clean)  # remover rt do inicio dos retweets
        tweet_clean = tweet_clean.strip()
        return tweet_clean