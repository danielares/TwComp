from django.views.generic import TemplateView
from django.core.files.storage import FileSystemStorage
from django.template.loader import render_to_string
from django.http import HttpResponse
import csv
import json

from weasyprint import HTML

from my_libs.create_charts_png import create_pie_chart, create_bar_chart, create_bar_chart_compare
from my_libs.word_cloud import wordCloud


class GeneratePdfView(TemplateView):
    
    def get(self, request, *args, **kwargs): 
        
        amoutTweets = request.session['number_of_tweets']
        chartsInfo = request.session['charts_info']
        qtd_tweets = request.session['charts_info']['qtd_tweets']
        colors = request.session['charts_info']['colors']
        labels = request.session['charts_info']['labels']
        options = json.loads(request.session['options'])
        tweets = json.loads(request.session['tweets'])
        
        search = options['search']
        
        wordcloud = wordCloud(tweets, search)
        pie = create_pie_chart(qtd_tweets, labels, colors, search)
        bar = create_bar_chart(labels, qtd_tweets, search, colors)
        
        
        html_string = render_to_string('tools/generate-pdf.html', {'term': search, 'amoutTweets': amoutTweets,
                                                                   'chartsInfo': chartsInfo, 'pieChart': pie,
                                                                   'barChart': bar, 'wordcloud': wordcloud,
                                                                   'type_of_analysis': options['type_of_analysis']})
             
        html = HTML(string=html_string, base_url=request.build_absolute_uri())
        
        #Para usar localmente
        #html.write_pdf(target='C:/Users/danie/Documents/projetos django/twitter 3 - DOCKER/tmp/relatorio_tweets.pdf')
        
        
        #PARA DEPLOY
        html.write_pdf(target='/tmp/relatorio_tweets.pdf')
        fs = FileSystemStorage('/tmp')
        #ADICIONAR FS. ANTES DO OPEN
        
        
        with fs.open('relatorio_tweets.pdf') as pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            #Faz o download do arquivo PDF
            #response['Content-Disposition'] = 'attachment; filename="relatorio_tweets.pdf"'
            
            #Abre o PDF direto no navegador
            response['Content-Disposition'] = 'inline; filename="relatorio_tweets.pdf"'
              
        return response


class GenerateComparePdfView(TemplateView):
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    
    def get(self, request, *args, **kwargs):   
        term1 = request.session['search1']
        term2 = request.session['search2']
        amoutTweets = request.session['number_of_tweets1']
        chartsInfo1 = request.session['charts_info1']
        chartsInfo2 = request.session['charts_info2']
        options = json.loads(request.session['options'])
        tweets1 = json.loads(request.session['tweets1'])
        tweets2 = json.loads(request.session['tweets2'])
        
        qtd_tweets1 = request.session['charts_info1']['qtd_tweets']
        colors1 = request.session['charts_info1']['colors']
        labels1 = request.session['charts_info1']['labels']
        
        qtd_tweets2 = request.session['charts_info2']['qtd_tweets']
        colors2 = request.session['charts_info2']['colors']
        labels2 = request.session['charts_info2']['labels']
        
        bar = create_bar_chart_compare(labels1, qtd_tweets1, term1,
                                       qtd_tweets2, term2)
        
        pie1 = create_pie_chart(qtd_tweets1, labels1, colors1, term1)
        pie2 = create_pie_chart(qtd_tweets2, labels2, colors2, term2)
        wordcloud1 = wordCloud(tweets1, term1)
        wordcloud2 = wordCloud(tweets2, term2)

        html_string = render_to_string('tools/generate-compare-pdf.html', {'term1': term1, 
                                                                            'term2': term2,
                                                                            'amoutTweets': amoutTweets,
                                                                            'chartsInfo1': chartsInfo1,
                                                                            'chartsInfo2': chartsInfo2,
                                                                            'barChart': bar,
                                                                            'pieChart1': pie1,
                                                                            'pieChart2': pie2,
                                                                            'wordcloud1': wordcloud1,
                                                                            'wordcloud2': wordcloud2,
                                                                            'type_of_analysis': options['type_of_analysis']})
        
        html = HTML(string=html_string, base_url=request.build_absolute_uri())
        
        #Usado localmente
        #html.write_pdf(target='C:/Users/danie/Documents/projetos django/twitter 3 - DOCKER/tmp/relatorio_tweets.pdf')
        
        
        #PARA DEPLOY
        html.write_pdf(target='/tmp/relatorio_compare_tweets.pdf')
        fs = FileSystemStorage('/tmp')
        #ADICIONAR FS. ANTES DO OPEN
    
        
        with fs.open('relatorio_compare_tweets.pdf') as pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            #Faz o download do arquivo PDF
            #response['Content-Disposition'] = 'attachment; filename="relatorio_tweets.pdf"'
            
            #Abre o PDF direto no navegador
            response['Content-Disposition'] = 'inline; filename="relatorio_compare_tweets.pdf"'
        
        return response


def generateCsv(request):
    search = request.session['search']
    tweets = json.loads(request.session['tweets'])

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=tweets.csv'
    
    # Encode UTF-8
    response.write(u'\ufeff'.encode('utf8'))
    
    # Create a csv writer
    writer = csv.writer(response)
    
    term = search
    
    #Add column headings for the csv file
    writer.writerow([term+': Tweet id', 'Tweet clean', 'Tweet language', 'Tweet date', 'Tweet analise', 'Tweet polaridade'])
    
    # Loop through the tweets
    for tweet in tweets:
        writer.writerow([tweet['tweet_id'], tweet['tweet_clean'], tweet['tweet_lang'], tweet['tweet_created_at'], 
                         tweet['tweet_analise'], tweet['tweet_analise'][0]])

        
    return response


def generateCsvCompare(request):
    search1 = request.session['search1']
    tweets1 = json.loads(request.session['tweets1'])
    
    search2 = request.session['search2']
    tweets2 = json.loads(request.session['tweets2'])
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=tweets.csv'
    
    # Encode UTF-8
    response.write(u'\ufeff'.encode('utf8'))
    
    # Create a csv writer
    writer = csv.writer(response)
    
    #Add column headings for the csv file term 1
    writer.writerow([search1+': Tweet id', ': Tweet clean', ': Tweet language', ': Tweet date', ': Tweet polaridade'])
    
    # Loop through the tweets of term 1
    for tweet in tweets1:
        writer.writerow([tweet['tweet_id'], tweet['tweet_clean'], tweet['tweet_lang'], tweet['tweet_created_at'], 
                         tweet['tweet_analise']])
        
        
    #Add column headings for the csv file term 2
    writer.writerow([search2+': Tweet id', ': Tweet clean', ': Tweet language', ': Tweet date', ': Tweet polaridade'])
    
    # Loop through the tweets of term 1
    for tweet in tweets2:
        writer.writerow([tweet['tweet_id'], tweet['tweet_clean'], tweet['tweet_lang'], tweet['tweet_created_at'], 
                         tweet['tweet_analise']])
        
    return response