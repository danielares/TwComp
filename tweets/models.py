from django.db import models

class Base(models.Model):
    criado = models.DateField('Data de Criação', auto_now_add=True)
    modificado = models.DateField('Data de Atualização', auto_now=True)
    ativo = models.BooleanField('Ativo?', default=True)
    
    class Meta:
        abstract = True
        
        
class TrainingBase(Base):
    nome = models.TextField('Texto', max_length=300)
    sentimento = models.CharField('Sentimento', max_length=100)
    
    def __str__(self):
        return self.Sentimento
