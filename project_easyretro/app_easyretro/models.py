from django.db import models

class Form(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
class Question(models.Model):
    FORM_TYPE_CHOICES = [
        ('linear', 'Escala Linear'),
        ('multiple', 'Múltipla Escolha'),
    ]

    form = models.ForeignKey(Form, related_name='questions', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    type = models.CharField(max_length=50, choices=FORM_TYPE_CHOICES)
    options = models.JSONField(blank=True, null=True)  # Para armazenar opções de múltipla escolha
    intensity = models.IntegerField(blank=True, null=True)  # Novo campo para intensidade

    def __str__(self):
        return self.title