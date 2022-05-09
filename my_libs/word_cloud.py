import io
import urllib, base64

from wordcloud import WordCloud
import nltk
nltk.download('stopwords')
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt

list_stopwords_portuguese = nltk.corpus.stopwords.words('portuguese')


# Função para criar a imagem word cloud
def wordCloud(tweets, searched_term):
    word_cloud = WordCloud(stopwords=list_stopwords_portuguese, mode = "RGBA", 
                           background_color=None, width = 1200, height=700, 
                           margin=1, max_words=200)
    
    # Adiciona todos os tweets em uma unica string que é usada para gerar a wordcloud
    all_tweets = ""
    for tweet in tweets:
        text = str(tweet['tweet_clean'])
        all_tweets += "".join(" "+text)
    
    # Adicionar o termo pesquisado a lista de stopwords e outras palavras, que não são mostradas na wordcloud
    my_list_stopwords = [searched_term, 'pra']
    list_stopwords_portuguese.extend(my_list_stopwords)
    
    '''
    Essa parte do código gera a imagem utilizando matplotlib e salva ela em um buffer
    para ser enviada como contexto para o front.
    '''
    word_cloud.generate(all_tweets)
    plt.figure(figsize=(12,7))
    plt.imshow(word_cloud, interpolation="bilinear", aspect='auto')
    plt.axis('off')
    plt.tight_layout(pad=0)
    buffer = io.BytesIO()
    plt.gcf().savefig(buffer, format='png', transparent=True, bbox_inches='tight', pad_inches = 0)
    buffer.seek(0)
    string = base64.b64encode(buffer.read())
    buffer.close()
    plt.close()
    word_cloud_image = 'data:image/png;base64,' + urllib.parse.quote(string)
    
    return word_cloud_image
