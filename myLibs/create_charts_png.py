import io
import urllib, base64

import numpy as np
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt


'''
Essa parte do código é responsavel por gerar as imagens png que são mostradas no relatório gerado em PDF
As imagens são salvas em um buffer e enviadas para o front como contexto.
'''

def create_pie_chart(number_of_tweets, polarity, colors, term_searched):
    buf = io.BytesIO()
    plt.figure(figsize=(6,5))
    plt.rcParams['text.color'] = 'black'
    plt.pie(number_of_tweets, labels=polarity, autopct='%1.1f%%', colors=colors)
    plt.title('Tweets sobre: '+term_searched, fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.savefig(buf, format='png')
    plt.axis('off')
    fig = plt.gcf()
    fig.savefig(buf, format='png', transparent=True, bbox_inches='tight', pad_inches = 0)
    buf.seek(0)
    string = base64.b64encode(buf.read())
    buf.close()
    pie_chart = 'data:image/png;base64,' + urllib.parse.quote(string)               
    return pie_chart


def create_bar_chart(polarity, number_of_tweets, term_searched, colors):
    buf = io.BytesIO()
    plt.figure(figsize=(7,4))
    plt.bar(polarity, number_of_tweets,  color=colors, edgecolor='black')
    plt.title('Tweets sobre: '+term_searched, fontsize=16, fontweight='bold')
    plt.xlabel('Sentimentos', fontsize=14, color='black')
    plt.ylabel('Quantidade de tweets', fontsize=14, color='black')
    plt.savefig(buf, format='png', transparent=True, pad_inches = 0)
    buf.seek(0)
    string = base64.b64encode(buf.read())
    buf.close()
    bar_chart = 'data:image/png;base64,' + urllib.parse.quote(string)               
    return bar_chart


def create_bar_chart_compare(labels1, number_of_tweets1, term1, 
                             number_of_tweets2, term2):
    buf = io.BytesIO()
    plt.figure(figsize=(7,4))
    x_axis = np.arange(len(labels1))
    plt.bar(x_axis -0.2, number_of_tweets1, 0.4, color="red", edgecolor='black', label=term1)
    plt.bar(x_axis +0.2, number_of_tweets2, 0.4, color="blue", edgecolor='black', label=term2)
    plt.xticks(x_axis, labels1)
    plt.legend()
    plt.title(term1+" X "+term2 , fontsize=16, fontweight='bold')
    plt.xlabel('Sentimentos', fontsize=14, color='black')
    plt.ylabel('Quantidade de tweets', fontsize=14, color='black')
    plt.savefig(buf, format='png', transparent=True, pad_inches = 0)
    buf.seek(0)
    string = base64.b64encode(buf.read())
    buf.close()
    bar_chart = 'data:image/png;base64,' + urllib.parse.quote(string)               
    return bar_chart