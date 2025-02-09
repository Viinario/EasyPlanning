from rest_framework import serializers
from .models import Form, Question

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'
        extra_kwargs = {
            'form': {'required': False}
        }

    def create(self, validated_data):
        return Question.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.type = validated_data.get('type', instance.type)
        instance.options = validated_data.get('options', instance.options)
        instance.intensity = validated_data.get('intensity', instance.intensity)
        instance.save()
        return instance

class FormSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True)

    class Meta:
        model = Form
        fields = '__all__'

    def create(self, validated_data):
        questions_data = validated_data.pop('questions')
        form = Form.objects.create(**validated_data)
        for question_data in questions_data:
            Question.objects.create(form=form, **question_data)
        return form
    
    def update(self, instance, validated_data):
        questions_data = validated_data.pop('questions')
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.save()

        # Atualizar perguntas
        keep_questions = []
        for question_data in questions_data:
            if 'id' in question_data:
                question = Question.objects.get(id=question_data['id'], form=instance)
                question.title = question_data.get('title', question.title)
                question.description = question_data.get('description', question.description)
                question.type = question_data.get('type', question.type)
                question.options = question_data.get('options', question.options)
                question.intensity = question_data.get('intensity', question.intensity)
                question.save()
                keep_questions.append(question.id)
            else:
                question = Question.objects.create(form=instance, **question_data)
                keep_questions.append(question.id)

        # Remover perguntas que não estão na lista de manutenção
        for question in instance.questions.all():
            if question.id not in keep_questions:
                question.delete()

        return instance