import io
import urllib, base64
import re
import heapq

import pandas as pd
from wordcloud import WordCloud
import nltk
nltk.download('stopwords')
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer

from my_libs.create_charts_png import create_bar_chart_frequency_words
from my_libs.html_chart import create_html_chart

list_stopwords_portuguese = nltk.corpus.stopwords.words('portuguese')

#https://towardsdatascience.com/how-to-make-word-clouds-in-python-that-dont-suck-86518cdcb61f
# Função para criar a imagem word cloud

def start_wc_tfidf(tweets, searched_term):
    tweets_tfidf = tfidf(tweets, searched_term)
    df_word_importance = word_importance(tweets_tfidf)
    word_cloud_image = wordCloud(tweets_tfidf)
    word_importance_image = create_bar_chart_frequency_words(df_word_importance.head(10))
    html_chart = create_html_chart(df_word_importance.head(20))
    
    return word_cloud_image, word_importance_image, html_chart
    
def wordCloud(tweets_tfidf):    
    word_cloud = WordCloud(background_color=None, width = 1200, height=700, max_words=200).generate_from_frequencies(tweets_tfidf.T.sum(axis=1))
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
    #print(vectorizer.vocabulary_)
    #print(vecs)
    #pd_vecs = pd.DataFrame.sparse.from_spmatrix(vecs)
    #print(pd_vecs)
    feature_names = vectorizer.get_feature_names()
    dense = vecs.todense()
    lst1 = dense.tolist()
    df = pd.DataFrame(lst1, columns=feature_names)
    return df

def word_importance(df):
    df_aux = df.T.sum(axis=1)
    df_aux2 = pd.DataFrame(df_aux)
    df_aux2 = df_aux2.sort_values(by=[0], ascending=False)
    return df_aux2

    