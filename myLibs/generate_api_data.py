def count_polarity(tweets):
    positive = 0
    neutral = 0
    negative = 0
    
    for tweet in tweets:
        if tweet['tweet_analise'][0] == 'positivo':
            positive += 1
        elif tweet['tweet_analise'][0] == 'neutro':
            neutral += 1
        else:
            negative += 1
            
    return positive, neutral, negative 


def count_sentiments(tweets):
    alegria = 0
    nojo = 0
    medo = 0
    raiva = 0
    surpresa = 0
    tristeza = 0
    
    for tweet in tweets:
        if tweet['tweet_analise'][0] == 'alegria':
            alegria += 1
        elif tweet['tweet_analise'][0] == 'nojo':
            nojo += 1
        elif tweet['tweet_analise'][0] == 'medo':
            medo += 1
        elif tweet['tweet_analise'][0] == 'raiva':
            raiva += 1
        elif tweet['tweet_analise'][0] == 'surpresa':
            surpresa += 1
        else:
            tristeza += 1

    return alegria, nojo, medo, raiva, surpresa, tristeza


def generate_simple_data(tweets):
    positive, neutral, negative = count_polarity(tweets)
             
    polaridade = ['Positivo', 'Neutro', 'Negativo']
    qtd_tweets = [positive, neutral, negative]
    colors = ['green','gray','red']
    
    return {"qtd_tweets": qtd_tweets, "labels": polaridade, "colors":colors}


def generate_advanced_data(tweets):
    alegria, nojo, medo, raiva, surpresa, tristeza = count_sentiments(tweets)
             
    polaridade = ['alegria', 'nojo', 'medo', 'raiva', 'surpresa', 'tristeza']
    qtd_tweets = [alegria, nojo, medo, raiva, surpresa, tristeza]
    colors = ['yellow','green', 'violet', 'red', 'blue', 'gray']
    
    return {"qtd_tweets": qtd_tweets, "labels": polaridade, "colors":colors}