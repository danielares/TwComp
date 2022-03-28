from django.contrib import admin

from .models import TrainingBase, TrainingBaseAdvanced

#@admin.register(TrainingBase)
class TrainingBaseAdmin(admin.ModelAdmin):
    list_display = ('Texto', 'Sentimento')
    
    
class TrainingBaseAdvancedAdmin(admin.ModelAdmin):
    list_display = ('Texto', 'Sentimento')


admin.site.register(TrainingBase)
admin.site.register(TrainingBaseAdvanced)
