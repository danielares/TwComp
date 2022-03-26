from myLibs.training_analysis import create_dict_training
from myLibs.generate_api_data import generate_advanced_data, generate_simple_data

def get_tweets(search, amoutTweets, option,
                consumerKey, consumerSecret, 
                accessToken, accessTokenSecret, bearerToken):
    
    if option == 'simple': chart_type = generate_simple_data
    elif option == 'advanced': chart_type = generate_advanced_data
    
    tweets = create_dict_training(option, search, amoutTweets, consumerKey, consumerSecret, 
                                    accessToken, accessTokenSecret, bearerToken)
    chartsInfo = chart_type(tweets)
    
    return tweets, chartsInfo