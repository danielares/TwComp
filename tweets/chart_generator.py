from importlib.metadata import metadata
from tkinter import font
from turtle import color
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
import pandas as pd


    
def count_polarity(tweets, term_searched):
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
    
    polaridade = ['Positivo', 'Neutro', 'Negativo']
    qtd_tweets = [positive, neutral, negative]
    colors = ['green','gray','red']
    explode = (0, 0, 0,) 
    
    plt.rcParams['text.color'] = 'white'
    plt.pie(qtd_tweets, labels=polaridade, autopct='%1.1f%%', explode=explode, colors=colors)
    plt.legend(polaridade, loc=3, frameon=True, facecolor='black')
    plt.title('Polaridade dos tweets', fontsize=16, fontweight='bold')
    plt.axis('equal')
    plt.tight_layout()
    plt.savefig('pages/static/images/temp/'+term_searched+'Pizza.png', transparent=True)
    plt.clf()
    
    
    plt.bar(1, positive, width=0.25, label = 'Positivo', color = 'g')
    plt.bar(1.5, neutral, width=0.25, label = 'Neutro', color = 'gray')
    plt.bar(2, negative, width=0.25, label = 'Negativo', color = 'r')
    plt.legend(frameon=True, facecolor='black')
    plt.title('Polaridade dos tweets', fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.savefig('pages/static/images/temp/'+term_searched+'Bar.png', transparent=True)
    plt.clf()
    
    return None