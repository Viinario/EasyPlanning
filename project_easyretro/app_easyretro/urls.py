from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FormViewSet, QuestionViewSet, AnswerViewSet


router = DefaultRouter()
router.register(r'forms', FormViewSet)
router.register(r'questions', QuestionViewSet)
router.register(r'answers', AnswerViewSet, basename='answer')

urlpatterns = [
    path('', include(router.urls)),
]