import re
import tweepy
from itertools import zip_longest


# Faz a autenticação utilizando o brarer token com o twitter atraves da biblioteca tweepy
def get_client(tokens):
    client = tweepy.Client(bearer_token=tokens)
    return client


def search_more_than_100_tweet(search_term, number_of_tweets, filter_retweets, filter_reply, tokens):

    client = get_client(tokens)

    # Campos de extensão opcionais buscados durante uma requisição na API do twitter
    expansions_options = ['author_id','referenced_tweets.id']
    tweet_fields_options = ['created_at','lang','geo', 'referenced_tweets']
    tweets_user_fields = ['username', 'location']


    if filter_retweets: search_term = search_term + ' -is:retweet'
    if filter_reply: search_term = search_term + ' -is:reply'
    tweets = []
    for tweet in tweepy.Paginator(client.search_recent_tweets, query=search_term+' lang:pt', tweet_fields=tweet_fields_options,
                                  expansions=expansions_options, user_fields=tweets_user_fields, max_results=100).flatten(limit=int(number_of_tweets)):
        tweets.append(tweet)

    results = []

    for tweet in tweets:
        try:
            tweet_dict = {}
            tweet_dict['tweet_id'] = tweet.id
            if tweet.text[:2] != "RT":
                tweet_dict['tweet_text'] = tweet.text
            else:
                tweet_dict['tweet_text'] = tweet.text
            tweet_dict['tweet_created_at'] = tweet.created_at
            tweet_dict['tweet_lang'] = tweet.lang
            tweet_dict['tweet_referenced_tweets'] = tweet.referenced_tweets
            results.append(tweet_dict)
        except:
            print('deu erro na coleta')

    return results



# Procura os tweets com base no termo pesquisado
def search_tweets(search_term, number_of_tweets, filter_retweets, filter_reply, tokens):

    # chama a função que cria o cliente com o qual fazemos as requisições a API do twitter
    client = get_client(tokens)

    # Campos de extensão opcionais buscados durante uma requisição na API do twitter
    expansions_options = ['author_id','referenced_tweets.id']
    tweet_fields_options = ['created_at','lang', 'text', 'referenced_tweets']
    tweets_user_fields = ['username', 'location']
    
    # Busca os tweets mais recentes
    # -is:retweet -> filtro para não pegar retweets
    # lang:pt -> para pegar somente tweets em portugues
    if filter_retweets: search_term = search_term + ' -is:retweet'
    if filter_reply: search_term = search_term + ' -is:reply'
    tweets = client.search_recent_tweets(query=search_term+' lang:pt', max_results=number_of_tweets, expansions=expansions_options,
                                         tweet_fields=tweet_fields_options, user_fields=tweets_user_fields)

    # loop para salvar os tweets coletados em um dicionario python
    results = []
    for tweet in tweets.data:
        try:
            tweet_dict = {}
            #tweet_dict['tweet_username'] = tweet_user.username
            #tweet_dict['tweet_location'] = tweet_user.location
            tweet_dict['tweet_id'] = tweet.id
            if tweet.text[:2] != "RT":
                tweet_dict['tweet_text'] = tweet.text
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
                        tweet_dict['tweet_text'] = retweet.text
            tweet_dict['tweet_created_at'] = tweet.created_at
            tweet_dict['tweet_lang'] = tweet.lang
            tweet_dict['tweet_referenced_tweets'] = tweet.referenced_tweets
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
        tweet_clean = re.sub("[^0-9A-Za-z ñÑÀàÁáÉéÍíÓóÚúÂâÊêÎîÔôÛûÃãÕõÇç@]", "", tweet_clean).lower()  # deixa somente os caracteres aceitos
        tweet_clean = re.sub(r"http\S+", "", tweet_clean)  # remove links
        tweet_clean = re.sub(r"@\S+", "", tweet_clean)  # remove @USERNAME
        #tweet_clean = re.sub(r"#\S+", "", tweet_clean)  # remove hashtags
        tweet_clean = re.sub(r"ñ", "não", tweet_clean)  # substitui ñ por não
        tweet_clean = re.sub(r"^B\S([rt]+)?", "", tweet_clean)  # remover rt do inicio dos retweets
        tweet_clean = tweet_clean.strip()
        return tweet_clean

#EMOTICONS_ALEGRIA = ['😀','😃','😄','😁','😆','😅','😂','🤣','😇','🥰','😍','😌','😋','☺️','🙃','🙂','😊',
                     #'😉','😘','😗','😙','😚','🤪','😜','😝','😛','🤑','😎','🤓','🥸','🥳','😏']
#EMOTICONS_TRISTEZA = [😐😑😒🙄😳😟😔😕🙁☹️🥺😣😖😫😩🥱😪😮‍💨😮]
#EMOTICONS_RAIVA = [😤😠😡🤬👺👹]
#EMOTICONS_NOJO = [🤢🤮]
#EMOTICONS_SURPREZA = [😱🤯😨😰😥]
#EMOTICONS_OUTROS = [👏🤲🙌👏🤝👍👎👊✊✌️]

