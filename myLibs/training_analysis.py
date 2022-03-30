import pandas as pd
import numpy as np
import nltk

from .data_processing import search_tweets, clean_tweet
from trainingBase.models import TrainingBase, TrainingBaseAdvanced
#from myLibs.training_base import training_base_advanced, training_base_simple

list_stopwords_portuguese = nltk.corpus.stopwords.words('portuguese')
np.transpose(list_stopwords_portuguese)


def remove_stop_words(texto):
    frases = []
    for (palavras, sentimento) in texto:
        # Criamos uma list compreheension para extrair apenas as palavras que não estão na lista_Stop
        semStop = [ p for p in palavras.split() if p not in list_stopwords_portuguese]
        # Inserindo as frases com os Labels (sentimento) já tratadas pela Lista_Stop
        frases.append((semStop, sentimento))
    return frases


def apply_stmmer(texto):
    stemmer = nltk.stem.RSLPStemmer()
    # Escolhido o RSLPS pois é especifico da lingua portuguesa
    frases_sem_Stemming = []
    for (palavras, sentimento) in texto:
        com_Stemming = [str(stemmer.stem(p)) for p in palavras.split() if p not in list_stopwords_portuguese]
        frases_sem_Stemming.append((com_Stemming, sentimento))
    return frases_sem_Stemming


def search_words(frases):
    todas_Palavras = []
    for (palavras, sentimento) in frases:
        todas_Palavras.extend(palavras)
    return todas_Palavras


def frequency_words(palavras):
    palavras = nltk.FreqDist(palavras)
    return palavras


def unique_words(frequencia):
    freq = frequencia.keys()
    return freq


def word_extractor(documento):
    # Utilizado set() para associar a variavel doc com o parâmetro que esta chegando
    global palavras_unicas_treinamento
    doc = set(documento)
    caracteristicas = {}
    for palavras in palavras_unicas_treinamento:
        caracteristicas['%s' % palavras] = (palavras in doc)
    return caracteristicas


def analyze_tweet(tweet, classificador):
    try:
        testeStemming = []
        stemmer = nltk.stem.RSLPStemmer()

        for (palavras_treinamento) in tweet.split():
            comStem = [palavra for palavra in palavras_treinamento.split()]
            testeStemming.append(str(stemmer.stem(comStem[0])))

        novo = word_extractor(testeStemming)

        distribuicao = classificador.prob_classify(novo)
        
        probable_feeling_bigger = 0
        
        for classe in distribuicao.samples():
            probable_feeling = distribuicao.prob(classe)
            if probable_feeling > probable_feeling_bigger:
                probable_feeling_bigger = probable_feeling
                classe_feeling = classe
        felling = classe_feeling, probable_feeling_bigger  
            
        return felling
    except:
        print('deu erro na analise')


def inicialize(option):
    global palavras_unicas_treinamento
    
    # if/else utilizado para utilizar o banco de dados da base de treinamento a avançada ou simples
    if option == 'simple': queryset = TrainingBase.objects.all()
    else: queryset = TrainingBaseAdvanced.objects.all()
    
    querysetvalues = queryset.values('texto', 'sentimento')
    training_base_list = list(querysetvalues)
    training_base_list2 = []
    for dict in training_base_list:
        training_base_list2.append(dict.values())
    frases_com_Stem_treinamento = apply_stmmer(training_base_list2)
     
    ''' Usado para utilizar dados do training_base.py no lugar do banco de dados
    if option == 'simple':
        training_base_df = pd.DataFrame(training_base_simple)
        training_base_df.columns = ['Phrase', 'Sentiment']
        frases_com_Stem_treinamento = apply_stmmer(training_base_simple)
    else: 
        training_base_df = pd.DataFrame(training_base_advanced)
        training_base_df.columns = ['Phrase', 'Sentiment']
        frases_com_Stem_treinamento = apply_stmmer(training_base_advanced)
    '''  
    
    palavras_treinamento = search_words(frases_com_Stem_treinamento)    
    frequencia_treinamento = frequency_words(palavras_treinamento)
    palavras_unicas_treinamento = unique_words(frequencia_treinamento)
    base_completa_treinamento = nltk.classify.apply_features(word_extractor, frases_com_Stem_treinamento)
    classificador = nltk.NaiveBayesClassifier.train(base_completa_treinamento)
    return classificador

def create_dict_training(option, query, amount, bearerToken):
    tweets = []
    tweets_dict = {}
    
    # retorna o classificador que foi criado com base na base de treinamento 
    # e sera utilizado como parametro para a função analyze_tweet
    classificador = inicialize(option) 
    
    # retorna todos os tweets em uma lista de dicionarios
    all_tweets = search_tweets(query, amount, bearerToken)

    for tweet in all_tweets:
        try:  
            tweet_clean = clean_tweet(tweet['text']) # limpa o tweet para ser analisado
            analise = analyze_tweet(tweet_clean, classificador) # analisa o tweet e retorna seu provavel sentimento
            
            # Cria um novo dicionario com o tweet já limpo e a analise já feita
            # E também com todas outras informçaões que já tinham no outro dicionario
            tweets_dict = {
               'tweet_id' : tweet['id'],
               'tweet_text': tweet['text'],
                'tweet_created_at': tweet['created_at'],
                'tweet_lang': tweet['lang'],
                'tweet_geo': tweet['geo'],
                'tweet_referenced_tweets': tweet['referenced_tweets'],
                'tweet_username': tweet['username'],
               'tweet_clean': tweet_clean,
               'tweet_analise': analise,
            }
            tweets.append(tweets_dict)
            
        except:
            print('deu erro')
            pass
    
    return tweets
