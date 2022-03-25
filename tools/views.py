from django.views.generic import TemplateView
from django.core.files.storage import FileSystemStorage
from django.template.loader import render_to_string
from django.http import HttpResponse
import csv

from weasyprint import HTML

from tweets.views import get_api 
from compareTweets.views import get_api as get_api_compare
from myLibs.create_charts_png import create_pie_chart, create_bar_chart
from myLibs.word_cloud import wordCloud


class GeneratePdfView(TemplateView):
    
    def get(self, request, *args, **kwargs):
        
        
        api = get_api()
        
        term = api['term']
        amoutTweets = api['amoutTweets']
        chartsInfo = api['chartsInfo']
        qtd_tweets = api['chartsInfo']['qtd_tweets']
        colors = api['chartsInfo']['colors']
        labels = api['chartsInfo']['labels']
        tweets = api['tweets']
        
        wordcloud = wordCloud(tweets, term)
        

        pie = create_pie_chart(qtd_tweets, labels, colors, term)
        
        bar = create_bar_chart(labels, qtd_tweets, term, colors)
        
        
        html_string = render_to_string('tools/generate-pdf.html', {'term': term, 'amoutTweets': amoutTweets,
                                                                   'chartsInfo': chartsInfo, 'pieChart': pie,
                                                                   'barChart': bar, 'wordcloud': wordcloud})
             
        html = HTML(string=html_string, base_url=request.build_absolute_uri())
        
        html.write_pdf(target='/tmp/relatorio_tweets.pdf')
        
        fs = FileSystemStorage('/tmp')
           
        
        
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
        fs = FileSystemStorage('tmp')
        
        api = get_api_compare()
        term1 = api['term1']
        term2 = api['term2']
        amoutTweets = api['amoutTweets']
        chartsInfo1 = api['chartsInfo1']
        chartsInfo2 = api['chartsInfo2']
        tweets1 = api['tweets1']
        tweets2 = api['tweets2']
        
        qtd_tweets1 = api['chartsInfo1']['qtd_tweets']
        colors1 = api['chartsInfo1']['colors']
        labels1 = api['chartsInfo1']['labels']
        
        qtd_tweets2 = api['chartsInfo2']['qtd_tweets']
        colors2 = api['chartsInfo2']['colors']
        labels2 = api['chartsInfo2']['labels']
        
        bar1 = create_bar_chart(labels1, qtd_tweets1, term1, colors1)
        bar2 = create_bar_chart(labels2, qtd_tweets2, term2, colors2)
        pie1 = create_pie_chart(qtd_tweets1, labels1, colors1, term1)
        pie2 = create_pie_chart(qtd_tweets2, labels2, colors2, term2)
        wordcloud1 = wordCloud(tweets1, term1)
        wordcloud2 = wordCloud(tweets2, term2)

        
        html_string = render_to_string('tools/generate-compare-pdf.html', {'term1': term1, 
                                                                   'term2': term2,
                                                                   'amoutTweets': amoutTweets,
                                                                   'chartsInfo1': chartsInfo1,
                                                                   'chartsInfo2': chartsInfo2,
                                                                   'barChart1': bar1,
                                                                   'barChart2': bar2,
                                                                   'pieChart1': pie1,
                                                                   'pieChart2': pie2,
                                                                   'wordcloud1': wordcloud1,
                                                                   'wordcloud2': wordcloud2})
        
        html = HTML(string=html_string, base_url=request.build_absolute_uri())
        html.write_pdf(target='/tmp/relatorio_compare_tweets.pdf')
        
        
        with fs.open('relatorio_compare_tweets.pdf') as pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            #Faz o download do arquivo PDF
            #response['Content-Disposition'] = 'attachment; filename="relatorio_tweets.pdf"'
            
            #Abre o PDF direto no navegador
            response['Content-Disposition'] = 'inline; filename="relatorio_compare_tweets.pdf"'
        
        return response


def generateCsv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=tweets.csv'
    
    # Encode UTF-8
    response.write(u'\ufeff'.encode('utf8'))
    
    # Create a csv writer
    writer = csv.writer(response)
    
    # Designate the Model
    api = get_api()

    #Add column headings for the csv file
    writer.writerow(['Tweet id', 'Tweet clean', 'Tweet language', 'Tweet date', 'Tweet polaridade'])
    
    # Loop through the tweets
    for tweet in api['tweets']:
        writer.writerow([tweet['tweet_id'], tweet['tweet_clean'], tweet['tweet_lang'], tweet['tweet_created_at'], tweet['tweet_analise']])
        
    return response


def generateCsvCompare(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=tweets.csv'
    
    # Encode UTF-8
    response.write(u'\ufeff'.encode('utf8'))
    
    # Create a csv writer
    writer = csv.writer(response)
    
    # Get api
    api = get_api_compare()

    term1 = api['term1']
    term2 = api['term2']
    
    #Add column headings for the csv file term 1
    writer.writerow([term1+': Tweet id', term1+': Tweet clean', term1+': Tweet language', term1+': Tweet date', term1+': Tweet polaridade'])
    
    # Loop through the tweets of term 1
    for tweet in api['tweets1']:
        writer.writerow([tweet['tweet_id'], tweet['tweet_clean'], tweet['tweet_lang'], tweet['tweet_created_at'], 
                         tweet['tweet_analise']])
        
        
    #Add column headings for the csv file term 2
    writer.writerow([term2+': Tweet id', term2+': Tweet clean', term2+': Tweet language', term2+': Tweet date', term2+': Tweet polaridade'])
    
    # Loop through the tweets of term 1
    for tweet in api['tweets2']:
        writer.writerow([tweet['tweet_id'], tweet['tweet_clean'], tweet['tweet_lang'], tweet['tweet_created_at'], 
                         tweet['tweet_analise']])
        
    return response