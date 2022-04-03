import pandas as pd

from my_libs.training_analysis import create_dict_training


'''
Função serve somente para chamar as funções de criar o dicionario e gerar dados para os graficos e retornar os dados
para a view que serão enviados para o front como contexto.

Uma vez que a função de criar o dicionario é chamada ela já chama todas outras função, 
Como: buscar tweets, limpar tweets, analisar tweets....
'''
def get_tweets(search_term, number_of_tweets, option, filter_retweets, filter_reply, bearer_token):
    
    tweets = create_dict_training(option, search_term, number_of_tweets, filter_retweets, filter_reply, bearer_token)
    charts_info = generate_data(tweets, option)
    
    return tweets, charts_info


'''
Função para contar a quantidade de tweets por categoria (positivo, neutro, negativo)
ou (alegria, nojo, raiva, surpresa, tristeza, medo)
'''
def generate_data(tweets, option):
    
    # if/else somente para escolher as cores que serão utilizadas, baseado na opçõa de analise
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
    for sentiment in df['tweet_analise']: sentiments.append(sentiment[0])
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
    
    '''
    Eu optei por salvar dessa forma(em listas) pq mudei um pouco a logica e anteriormente os valores eram entregue em lista
    Para não ter que mudar nesse momento salve dessa forma..
    Mas provavelmente ainda sera alterado para funcionar de maneira mais simples
    '''
    
    return {"qtd_tweets": count_sentiments_list,
            "labels": labels, 
            "colors":colors}
