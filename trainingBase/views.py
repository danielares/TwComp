from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.contrib.admin.views.decorators import staff_member_required
import pandas as pd
import csv
import json
from itertools import zip_longest

from trainingBase.models import TrainingBase, TrainingBaseAdvanced
from my_libs.training_analysis import create_dict_training

fs = FileSystemStorage(location='tmp/')


@method_decorator(staff_member_required, name='dispatch')
class TrainingBaseView(TemplateView):
    template_name = 'trainingBase/training-base.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    

@method_decorator(staff_member_required, name='dispatch')
class UploadBaseView(TemplateView):
    template_name = 'trainingBase/upload-training-base.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def post(self, request, **kwargs):
        try:
            file = request.FILES['file']
            option = request.POST['Options']
            
            #USADO PARA DEPLOY - COMENTAR PARA USAR LOCALMENTE
            content = file.read()
            file_content = ContentFile(content)
            file_name = fs.save(
                "_temp.csv", file_content
            )
            tmp_file = fs.path(file_name)
            
            csv_file = open(tmp_file, errors="ignore")
            csv.reader(csv_file)
            #USADO PARA DEPLOY - FIM
            
            # PARA USAR LOCALMENTE TROCAR NOME 'csv_file' para somente 'file' 
            if not csv_file.name.endswith('.csv'):
                messages.error(request, 'Você deve enviar um arquivo csv')
                return render(request, self.template_name)
            
            data_frame = pd.read_csv(csv_file, sep=';')
            
            if option == 'simple': training_base = TrainingBase
            else: training_base = TrainingBaseAdvanced
            
            for (texto, sentimento) in zip_longest(data_frame['texto'], data_frame['sentimento']):
                training_base.objects.create(texto=texto, sentimento=sentimento)
            
            messages.success(request, 'Base de treinamento adicionada!')
            return render(request, self.template_name)
        except:
            messages.error(request, 'Algum erro ocorreu.')
            return render(request, self.template_name)
            
      
@method_decorator(staff_member_required, name='dispatch')
class SearchTweetsTrainingView(TemplateView):
    template_name = 'trainingBase/search-tweets-training.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        positivo = TrainingBase.objects.filter(sentimento='positivo').count()
        neutro = TrainingBase.objects.filter(sentimento='neutro').count()
        negativo = TrainingBase.objects.filter(sentimento='negativo').count()
        
        alegria = TrainingBaseAdvanced.objects.filter(sentimento='alegria').count()
        nojo = TrainingBaseAdvanced.objects.filter(sentimento='nojo').count()
        medo = TrainingBaseAdvanced.objects.filter(sentimento='medo').count()
        raiva = TrainingBaseAdvanced.objects.filter(sentimento='raiva').count()
        surpresa = TrainingBaseAdvanced.objects.filter(sentimento='surpresa').count()
        tristeza = TrainingBaseAdvanced.objects.filter(sentimento='tristeza').count()
        
        context['trainingBaseSimple'] = positivo, neutro, negativo
        context['trainingBaseAdvanced'] = alegria, nojo, medo, raiva, surpresa, tristeza
        
        return context
    

@method_decorator(staff_member_required, name='dispatch')
class ViewTweetsTrainingView(TemplateView):
    template_name = 'trainingBase/view-tweets-training.html'
    
    def post(self, request, **kwargs):    
        options = {}
        options['search'] = request.POST['searched']
        options['number_of_tweets'] = request.POST['amoutTweets']
        options['type_of_analysis'] = request.POST['inlineRadioOptions']
        options['filter_retweets'] = True
        options['filter_reply'] = True
        user = self.request.user
        
        if not options['search']:
            messages.error(request, 'Você deve pesquisar algo')
            return redirect('search-tweets-training')
        tweets, locations = create_dict_training(user, options)
        
        request.session['type_of_analysis'] = options['type_of_analysis']
        request.session['tweets'] = json.dumps(tweets, indent=4, sort_keys=True, default=str)
        print('TWEETS',tweets)
        context = super().get_context_data(**kwargs)
        context['tweets'] = tweets
        context['option'] = options['type_of_analysis']
        return render(request, self.template_name, context)


@method_decorator(staff_member_required, name='dispatch')
class TrainingBaseSuccessView(TemplateView):
    template_name = 'trainingBase/training-success.html'
    
    def post(self, request, **kwargs):
        type_of_analysis = request.session['type_of_analysis']
        tweets = json.loads(request.session['tweets'])
        all_add_tweets = []
        context = super().get_context_data(**kwargs)
        
        for tweet in tweets:
            addTweetDB = 'addTweetDB_' + str(tweet['tweet_id'])
            label = 'label_' + str(tweet['tweet_id'])
            tweetDB = 'tweetDB_' + str(tweet['tweet_id'])
            
            try: addTweetDB = request.POST[addTweetDB]
            except: addTweetDB = False
            if addTweetDB:
                try: 
                    value_label = request.POST[label]
                    text_tweetDB = request.POST[tweetDB]
                    
                    if type_of_analysis == 'simple': training_base = TrainingBase
                    else: training_base = TrainingBaseAdvanced
                    training_base.objects.create(texto=text_tweetDB, sentimento=value_label)
                    
                    all_add_tweets.append({'tweet': text_tweetDB, 'sentimento': value_label})
                    
                except: 
                    print('ERRO AO ADICIONAR A BASE DE DADOS')
        context['tweet'] = all_add_tweets
        return render(request, self.template_name, context)
    

def generateCsvTrainingBase(request):
    option = request.POST['gerar_csv']
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=base de treinamento.csv'
    
    # Encode UTF-8
    response.write(u'\ufeff'.encode('utf8'))
    
    # Create a csv writer
    writer = csv.writer(response, delimiter=';')
    
    # Designate the Model
    if option == "CSV Simples":
        objects = TrainingBase.objects.all()
    else:
        objects = TrainingBaseAdvanced.objects.all()
        
    objects = objects.values()

    df = pd.DataFrame(objects)

    writer.writerow(['texto', 'sentimento'])
    #writer.writerows([df['texto'], df['sentimento']])

    for (texto, sentimento) in zip_longest(df['texto'], df['sentimento']):
        writer.writerow([texto, sentimento])
        
    return response