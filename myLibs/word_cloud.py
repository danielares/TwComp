
import io
import urllib, base64

from wordcloud import WordCloud
import nltk
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt

list_stopwords_portuguese = nltk.corpus.stopwords.words('portuguese')

def wordCloud(tweets, term):
    
    wc = WordCloud(stopwords=list_stopwords_portuguese, mode = "RGBA", 
                   background_color=None, width = 1200, height=700, margin=1, max_words=100)
    
    # Adiciona todos os tweets em uma unica string que é usada para gerar a wordcloud
    all_tweets = ""
    for tweet in tweets:
        text = str(tweet['tweet_clean'])
        all_tweets = all_tweets + " " + text

    # Adicionar o termo pesquisado a lista de stopwords, que não são mostradas na wordcloud
    list_stopwords_portuguese.append(term)
    
    '''
    Essa parte do código gera a imagem utilizando matplotlib e salva ela em um buffer
    para ser enviada como contexto para o front.
    '''
    wc.generate(all_tweets)
    plt.figure(figsize=(12,7))
    plt.imshow(wc, interpolation="bilinear", aspect='auto')
    plt.axis('off')
    plt.tight_layout(pad=0)
    buf = io.BytesIO()
    plt.gcf().savefig(buf, format='png', transparent=True, bbox_inches='tight', pad_inches = 0)
    buf.seek(0)
    string = base64.b64encode(buf.read())
    buf.close()
    plt.close()
    word_cloud_image = 'data:image/png;base64,' + urllib.parse.quote(string)
    
    return word_cloud_image
