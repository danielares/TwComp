from numpy import average
import pandas as pd
from geopy.geocoders import Nominatim
from datetime import datetime

from opencage.geocoder import OpenCageGeocode

from my_libs.training_analysis import create_dict_training


def get_tweets(api_access_tokens, options):
    
    tweets, locations = create_dict_training(api_access_tokens, options)
    charts_info = generate_data(tweets, options['type_of_analysis'])
    probability = probability_average(tweets)
    tweets_to_show = get_tweets_to_show(tweets)
    if options['option_maps']: geo_location = get_geo_location(locations)
    else: geo_location = False
    
    context_infos = {
        'tweets': tweets,
        'charts_info': charts_info,
        'probability': probability,
        'geo_location': geo_location,
        'options': options,
        'tweets_to_show': tweets_to_show,
        'data_time': datetime.today()
    }
    print(geo_location)
    return charts_info, context_infos


'''
Função para contar a quantidade de tweets por categoria (positivo, neutro, negativo)
ou (alegria, nojo, raiva, surpresa, tristeza, medo)
'''
def generate_data(tweets, option):
    # if/else para escolher as cores que serão utilizadas, baseado na opçõa de analise
    # e também para selecionar as labels do tipo de análise
    if option == 'simple': 
        colors = ['red','gray','green']
        all_labels = ['negativo', 'neutro', 'positivo']
    elif option == 'advanced': 
        colors = ['yellow', 'violet', 'green',  'red', 'blue', 'gray']
        all_labels = ['alegria', 'medo', 'nojo', 'raiva', 'surpresa', 'tristeza']
    
    # Cria um data frame com a lista de dicionarios (cada dicionario representa um tweet)
    df = pd.DataFrame(tweets)
    
    # Cria uma nova coluna no data frame que contem comente o sentimento, exemplo: alegria
    # Na coluna já existente também contem a probabilidade da analise estar certa.
    sentiments = []
    for sentiment in df['tweet_analise']: 
        sentiments.append(sentiment[0])
    df['sentiment'] = sentiments
    
    # Cria um dicionario com o numero de valores por sentimento
    count_sentiments = df['sentiment'].value_counts().to_dict()

    # Adiciona o valor 0 para os tweets que não estão no dicionario (para que no Compare Tweets os 2 termos tenham os mesmos labels)
    for single_label in all_labels:
        if single_label not in count_sentiments.keys():
            count_sentiments[single_label] = 0
    
    # Deixa o dicionario em ordem alfabetica(Baseado nas chaves do dicionario) isso evita que elementos fique na posição errada
    # no Compare Tweets
    count_sentiments = {key: value for key, value in sorted(count_sentiments.items())}

    # Lista somente com as chaves do dicionario
    labels = [label for label in count_sentiments.keys()]
    
    # Lista somente com os valores do dicionario
    count_sentiments_list = list(count_sentiments.values())
    return {"qtd_tweets": count_sentiments_list,
            "labels": labels, 
            "colors":colors}


def probability_average(tweets):
    average = 0
    quantity = 0
    for tweet in tweets:
        average += tweet['tweet_analise'][1]
        quantity += 1
    return round((average/quantity) * 100, 2)


def get_geo_location(locations):
    for location in locations:
        try:
            address = location['location']
            geolocator = Nominatim(user_agent="TwComp")
            geo_location = geolocator.geocode(address)
            location['address'] = geo_location.address
            location['latitude'] = geo_location.latitude
            location['longitude'] = geo_location.longitude
        except:
            print('Endereço não encontrado')
    
    '''key = "e1aa1c586c5241c0a61ae3984c3929a1"
    geocoder = OpenCageGeocode(key)
    for location in locations:
        try:
            address = location['location']
            results = geocoder.geocode(address)
            location['address'] = address
            location['latitude'] = results[0]['geometry']['lat']
            location['longitude'] = results[0]['geometry']['lng']
            print(results[0])
        except:
            print('Endereço não encontrado')'''
    return locations


def get_tweets_to_show(tweets):  
    list_tweets_to_show = []
    
    for tweet in tweets:
        if len(list_tweets_to_show) < 6:
            dict_tweets_to_show = {}
            dict_tweets_to_show['tweet_id'] = tweet['tweet_id']
            dict_tweets_to_show['tweet_analise'] = tweet['tweet_analise']
            list_tweets_to_show.append(dict_tweets_to_show)
            
    return list_tweets_to_show