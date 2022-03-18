import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt


def create_pie_chart(qtd_tweets, polaridade, explode, colors, term_searched):
    plt.rcParams['text.color'] = 'black'
    plt.pie(qtd_tweets, labels=polaridade, autopct='%1.1f%%', explode=explode, colors=colors)
    #plt.legend(polaridade, loc=3, frameon=True, facecolor='black')
    plt.title('Gráfico de pizza', fontsize=16, fontweight='bold')
    plt.axis('equal')
    plt.tight_layout()
    plt.savefig('pages/static/images/temp/'+term_searched+'Pizza.png', transparent=True)
    plt.clf()
    
       
def create_bar_chart(polaridade, qtd_tweets, term_searched, colors):
    plt.bar(qtd_tweets, polaridade, color=colors, edgecolor='black')
    #plt.legend(frameon=True, facecolor='black')
    plt.title('Gráfico de barras', fontsize=16, fontweight='bold')
    plt.xlabel('Sentimentos', fontsize=14, color='black')
    plt.ylabel('Quantidade de tweets', fontsize=14, color='black')
    plt.tight_layout()
    plt.savefig('pages/static/images/temp/'+term_searched+'Bar.png', transparent=True)
    plt.clf()


def count_polarity(tweets):
    positive = 0
    neutral = 0
    negative = 0
    
    for tweet in tweets:
        if tweet['polaridade'] == 'positive':
            positive += 1
        elif tweet['polaridade'] == 'neutral':
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
        elif tweet['tweet_analise'][0] == 'tristeza':
            tristeza += 1

    return alegria, nojo, medo, raiva, surpresa, tristeza


def create_chart(tweets, term_searched):
    positive, neutral, negative = count_polarity(tweets)
             
    polaridade = ['Positivo', 'Neutro', 'Negativo']
    qtd_tweets = [positive, neutral, negative]
    colors = ['green','gray','red']
    explode = (0, 0, 0,) 
    
    create_pie_chart(qtd_tweets, polaridade, explode, colors, term_searched)
    create_bar_chart(qtd_tweets, polaridade,  term_searched, colors)
    
    return {"qtd_tweets": qtd_tweets, "labels": polaridade, "colors":colors}


def create_chart_training(tweets, term_searched):
    alegria, nojo, medo, raiva, surpresa, tristeza = count_sentiments(tweets)
             
    polaridade = ['alegria', 'nojo', 'medo', 'raiva', 'surpresa', 'tristeza']
    qtd_tweets = [alegria, nojo, medo, raiva, surpresa, tristeza]
    colors = ['yellow','green', 'violet', 'red', 'blue', 'gray']
    explode = (0, 0, 0, 0, 0, 0) 
    
    create_pie_chart(qtd_tweets, polaridade, explode, colors, term_searched+'Training')
    create_bar_chart(qtd_tweets, polaridade, term_searched+'Training', colors)
    
    return {"qtd_tweets": qtd_tweets, "labels": polaridade, "colors":colors}