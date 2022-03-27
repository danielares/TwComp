import pandas as pd

from myLibs.training_analysis import create_dict_training


def get_tweets(search, amoutTweets, option, bearerToken):
    
    tweets = create_dict_training(option, search, amoutTweets, bearerToken)
    chartsInfo = generate_data(tweets, option)
    
    return tweets, chartsInfo


def generate_data(tweets, option):
    
    if option == 'simple': colors = ['green','gray','red']
    elif option == 'advanced': colors = ['yellow','green', 'violet', 'red', 'blue', 'gray']
    
    # Convert a List of dictionaries using from_records() method.
    df = pd.DataFrame(tweets)
    
    sentimentos = []
    for sentiment in df['tweet_analise']: sentimentos.append(sentiment[0])
    df['sentiment'] = sentimentos
    
    count_sentiments = df['sentiment'].value_counts()
    count_sentiments_dict = count_sentiments.to_dict()
    labels = [label for label in count_sentiments_dict.keys()]
    count_sentiments_list = count_sentiments.to_list()
    
    return {"qtd_tweets": count_sentiments_list,
            "labels": labels, 
            "colors":colors}