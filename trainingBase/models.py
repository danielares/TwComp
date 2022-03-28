from django.db import models

class Base(models.Model):
    criado = models.DateField('Data de Criação', auto_now_add=True)
    modificado = models.DateField('Data de Atualização', auto_now=True)
    ativo = models.BooleanField('Ativo?', default=True)
    
    class Meta:
        abstract = True
        
        
class TrainingBase(Base):
    LABELS = (
        ('positivo', 'positivo'),
        ('neutro', 'neutro'),
        ('negativo', 'negativo'),
    )
    texto = models.TextField('Texto', max_length=300)
    sentimento = models.CharField('Sentimento', choices=LABELS, max_length=20)
    
    def __str__(self):
        return f"{self.texto}, {self.sentimento}"


class TrainingBaseAdvanced(Base):
    LABELS = (
        ('alegria', 'alegria'),
        ('nojo', 'nojo'),
        ('medo', 'medo'),
        ('raiva', 'raiva'),
        ('surpresa', 'surpresa'),
        ('tristeza', 'tristeza'),
    )
    texto = models.TextField('Texto', max_length=300)
    sentimento = models.CharField('Sentimento', choices=LABELS, max_length=20)
    
    def __str__(self):
        return f"{self.texto}, {self.sentimento}"