import tweepy


# Faz a autenticação utilizando o brarer token com o twitter atraves da biblioteca tweepy
def get_client(api_access_tokens):
    client = tweepy.Client(bearer_token=api_access_tokens)
    return client


def search_more_than_100_tweet(api_access_tokens, options):

    client = get_client(api_access_tokens)

    # Campos de extensão opcionais buscados durante uma requisição na API do twitter
    expansions_options = ['author_id','referenced_tweets.id']
    tweet_fields_options = ['created_at','lang','geo', 'referenced_tweets']
    tweets_user_fields = ['username', 'location']


    # Busca os tweets mais recentes
    # -is:retweet -> filtro para não pegar retweets
    # lang:pt -> para pegar somente tweets em portugues
    query_search = options['search']
    if options['filter_retweets']: 
        query_search += "".join(" -is:retweet")
    if options['filter_reply']: 
        query_search += "".join(" -is:reply")
    
    tweets = []
    for tweet in tweepy.Paginator(client.search_recent_tweets, 
                                  query=query_search+' lang:pt', 
                                  tweet_fields=tweet_fields_options,
                                  expansions=expansions_options, 
                                  user_fields=tweets_user_fields, 
                                  max_results=100).flatten(limit=int(options['number_of_tweets'])):
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
            
    #locations = get_locations(tweets)
    locations = []

    return results, locations


# Procura os tweets com base no termo pesquisado
def search_tweets(api_access_tokens, options):
    # chama a função que cria o cliente com o qual fazemos as requisições a API do twitter
    client = get_client(api_access_tokens)
    # Campos de extensão opcionais buscados durante uma requisição na API do twitter
    expansions_options = ['author_id','referenced_tweets.id']
    tweet_fields_options = ['created_at','lang', 'text', 'referenced_tweets']
    tweets_user_fields = ['username', 'location']
    
    # Busca os tweets mais recentes
    # -is:retweet -> filtro para não pegar retweets
    # lang:pt -> para pegar somente tweets em portugues
    query_search = options['search']
    if options['filter_retweets']: 
        query_search += "".join(" -is:retweet")
    if options['filter_reply']: 
        query_search += "".join(" -is:reply")

    tweets = client.search_recent_tweets(query=query_search+' lang:pt', 
                                         max_results=options['number_of_tweets'], 
                                         expansions=expansions_options,
                                         tweet_fields=tweet_fields_options, 
                                         user_fields=tweets_user_fields)

    # loop para salvar os tweets coletados em uma lista de dicionario
    results = []
    for tweet in tweets.data:
        try:
            tweet_dict = {}
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

    locations = get_locations(tweets)
    
    return results, locations


def get_locations(tweets):
    locations = []
    for user, tweet in zip(tweets.includes['users'], tweets.data):
        if user.location != None:
            location_dict = {}
            location_dict['user'] = user.username
            location_dict['location'] = user.location
            location_dict['tweet_id'] = tweet.id
            location_dict['tweet_text'] = tweet.text
            locations.append(location_dict)
    return locations