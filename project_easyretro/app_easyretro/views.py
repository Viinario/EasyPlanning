from rest_framework import viewsets
from rest_framework.response import Response
from .models import Form, Question
from .serializers import FormSerializer, QuestionSerializer

class FormViewSet(viewsets.ModelViewSet):
    queryset = Form.objects.all()
    serializer_class = FormSerializer

class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

class AnswerViewSet(viewsets.ViewSet):
    def create(self, request):
        answers = request.data.get("answers", [])
        results = []
        for answer in answers:
            question = Question.objects.get(id=answer["question_id"])
            correct = (
                question.type == "multiple" and question.options[0] == answer["answer"]
            )
            results.append({"question_id": question.id, "correct": correct})
        return Response({"results": results})