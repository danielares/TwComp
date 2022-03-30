from django.contrib import admin

from .models import TrainingBase, TrainingBaseAdvanced

@admin.register(TrainingBase)
class TrainingBaseAdmin(admin.ModelAdmin):
    model = TrainingBase
    list_display = ('id', 'texto', 'sentimento')
    
    
@admin.register(TrainingBaseAdvanced) 
class TrainingBaseAdvancedAdmin(admin.ModelAdmin):
    model = TrainingBaseAdvanced
    list_display = ('id', 'texto', 'sentimento')
