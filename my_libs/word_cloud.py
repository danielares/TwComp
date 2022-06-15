import io
import urllib, base64

import pandas as pd
from wordcloud import WordCloud
import nltk
nltk.download('stopwords')
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer


list_stopwords_portuguese = nltk.corpus.stopwords.words('portuguese')

#https://towardsdatascience.com/how-to-make-word-clouds-in-python-that-dont-suck-86518cdcb61f
# Função para criar a imagem word cloud
def wordCloud(tweets, searched_term):    
    tweets_tfidf = tfidf(tweets, searched_term)
    word_cloud = WordCloud(background_color=None, width = 1200, height=700, max_words=200).generate_from_frequencies(tweets_tfidf.T.sum(axis=1))
    #word_cloud.recolor(color_func = black_color_func)    
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

def tfidf(tweets, searched_term):
    df = pd.DataFrame(tweets)
    df = df['tweet_clean']
    lista = df.values.tolist()
    my_list_stopwords = [searched_term.lower(), 'pra', 'tá', 'acho', 'da', 'chegue', 'to', 'ter', 'tá']
    list_stopwords_portuguese.extend(my_list_stopwords)
    vectorizer = TfidfVectorizer(stop_words=list_stopwords_portuguese, ngram_range = (1,1), min_df = .01)
    vecs = vectorizer.fit_transform(lista)
    feature_names = vectorizer.get_feature_names()
    dense = vecs.todense()
    lst1 = dense.tolist()
    df = pd.DataFrame(lst1, columns=feature_names)
    return df


'''
def black_color_func(word, font_size, position,orientation,random_state=None, **kwargs):
    return("hsl(0,100%, 1%)")
'''