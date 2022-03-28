import pandas as pd

from myLibs.training_analysis import create_dict_training


def get_tweets(search, amoutTweets, option, bearerToken):
    
    tweets = create_dict_training(option, search, amoutTweets, bearerToken)
    chartsInfo = generate_data(tweets, option)
    
    return tweets, chartsInfo


def generate_data(tweets, option):
    
    if option == 'simple': colors = ['red','gray','green']
    elif option == 'advanced': colors = ['gray', 'violet', 'green',  'red', 'blue', 'yellow']
    
    # Convert a List of dictionaries using from_records() method.
    df = pd.DataFrame(tweets)
    
    sentiments = []
    for sentiment in df['tweet_analise']: sentiments.append(sentiment[0])
    df['sentiment'] = sentiments
    
    count_sentiments = df['sentiment'].value_counts().to_dict()
    
    # List with dictionary keys
    labels = [label for label in count_sentiments.keys()]
    
    # List with dictionary values
    count_sentiments_list = list(count_sentiments.values())
    
    return {"qtd_tweets": count_sentiments_list,
            "labels": labels, 
            "colors":colors}