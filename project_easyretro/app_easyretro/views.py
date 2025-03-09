from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Form, Question, Answer
from .serializers import FormSerializer, QuestionSerializer, AnswerSerializer


class FormViewSet(viewsets.ModelViewSet):
    queryset = Form.objects.all()
    serializer_class = FormSerializer

class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

class AnswerViewSet(viewsets.ViewSet):
    def create(self, request):
        # Extract the answers list from the payload
        answers_data = request.data.get("answers")
        if answers_data is None:
            return Response(
                {"error": "No answers provided."},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = AnswerSerializer(data=answers_data, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request):
        form_id = request.query_params.get('formId')
        if not form_id:
            return Response(
                {"error": "Query parameter 'formId' is required."},
                status=status.HTTP_400_BAD_REQUEST
            )
        answers = Answer.objects.filter(form_id=form_id)
        serializer = AnswerSerializer(answers, many=True)
        return Response(serializer.data)
