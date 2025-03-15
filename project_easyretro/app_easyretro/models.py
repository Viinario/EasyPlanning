from django.db import models

class Form(models.Model):
    project_name = models.CharField(max_length=255)
    sprint = models.IntegerField(choices=[(i, f"Sprint {i}") for i in range(1, 11)])
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.project_name
    
class Question(models.Model):
    FORM_TYPE_CHOICES = [
        ('linear', 'Escala Linear'),
        ('multiple', 'Múltipla Escolha'),
    ]

    form = models.ForeignKey(Form, related_name='questions', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    type = models.CharField(max_length=50, choices=FORM_TYPE_CHOICES)
    options = models.JSONField(blank=True, null=True)
    intensity = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.title

class Answer(models.Model):
    form = models.ForeignKey(Form, related_name='answers', on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.JSONField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Answer for {self.question} on {self.form}"
