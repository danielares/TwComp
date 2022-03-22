
from wordcloud import WordCloud
import nltk

import io
import urllib, base64

import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt

list_stopwords_portuguese = nltk.corpus.stopwords.words('portuguese')

#mask = np.array(Image.open("/content/mask.png"))

def wordCloud(tweets, term):
    all_tweets = ""
    wc = WordCloud(stopwords=list_stopwords_portuguese, mode = "RGBA", 
                   background_color=None, width = 1200, height=700, margin=1, max_words=300)
    
    for tweet in tweets:
        text = str(tweet['tweet_clean'])
        all_tweets = all_tweets + " " + text

    wc.generate(all_tweets)
    #wc.to_file('pages/static/images/temp/wc'+ term +'.png')
    
    plt.figure(figsize=(12,7))
    plt.imshow(wc, interpolation="bilinear", aspect='auto')
    plt.axis('off')
    fig = plt.gcf()
    buf = io.BytesIO()
    fig.savefig(buf, format='png', transparent=True, bbox_inches='tight', pad_inches = 0)
    buf.seek(0)
    string = base64.b64encode(buf.read())
    buf.close()
    uri = 'data:image/png;base64,' + urllib.parse.quote(string)
   
                          
    return uri
