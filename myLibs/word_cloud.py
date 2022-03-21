from wordcloud import WordCloud
import nltk

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
    wc.to_file('media/images/wc'+ term +'.png')
    
    return None