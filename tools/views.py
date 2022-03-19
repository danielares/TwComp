from urllib import response
from django.views.generic import TemplateView
from django.core.files.storage import FileSystemStorage
from django.template.loader import render_to_string
from django.http import HttpResponse
import requests
import json

from weasyprint import HTML

from tweets.views import get_api


class GeneratePdfView(TemplateView):
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    
    def get(self, request, *args, **kwargs):
        fs = FileSystemStorage('tmp')
        
        api = get_api()
        term = api['term']
        amoutTweets = api['amoutTweets']
        chartsInfo = api['chartsInfo']

        
        html_string = render_to_string('tools/generate-pdf.html', {'term': term, 'amoutTweets': amoutTweets,
                                                                   'chartsInfo': chartsInfo})
        
        html = HTML(string=html_string, base_url=request.build_absolute_uri())
        html.write_pdf(target='tmp/relatorio_tweets.pdf')
        
        
        with fs.open('relatorio_tweets.pdf') as pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            #Faz o download do arquivo PDF
            #response['Content-Disposition'] = 'attachment; filename="relatorio_tweets.pdf"'
            
            #Abre o PDF direto no navegador
            response['Content-Disposition'] = 'inline; filename="relatorio_tweets.pdf"'
        
        return response


class GenerateCsvView(TemplateView):
    template_name = 'tools/generate-csv.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
