from django.contrib import admin

from .models import TrainingBase

#@admin.register(TrainingBase)
class TrainingBaseAdmin(admin.ModelAdmin):
    list_display = ('Texto', 'Sentimento')
    

admin.site.register(TrainingBase)
