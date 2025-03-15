from rest_framework import serializers
from .models import Form, Question, Answer

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
        instance.project_name = validated_data.get('project_name', instance.project_name)
        instance.sprint = validated_data.get('sprint', instance.sprint)
        instance.description = validated_data.get('description', instance.description)
        instance.save()

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

        for question in instance.questions.all():
            if question.id not in keep_questions:
                question.delete()

        return instance

class AnswerSerializer(serializers.ModelSerializer):
    question_description = serializers.CharField(source='question.description', read_only=True)
    question_type = serializers.CharField(source='question.type', read_only=True)
    project_name = serializers.CharField(source='form.project_name', read_only=True)
    sprint = serializers.IntegerField(source='form.sprint', read_only=True)
    multiple_options = serializers.ListField(
        child=serializers.CharField(),
        source='question.options',
        read_only=True
    )

    class Meta:
        model = Answer
        fields = [
            'id',
            'form',
            'project_name',
            'sprint',
            'question',
            'answer',
            'question_description',
            'question_type',
            'multiple_options',
            'submitted_at'
        ]

    def validate(self, data):
        question = data.get('question')
        answer_value = data.get('answer')
        if question is None:
            raise serializers.ValidationError("Question must be provided.")

        if question.type == "multiple":
            if question.options is None or answer_value not in question.options:
                raise serializers.ValidationError("Answer must be one of the available options.")
        elif question.type == "linear":
            try:
                int(answer_value)
            except (ValueError, TypeError):
                raise serializers.ValidationError("Answer must be an integer for linear questions.")
        return data
