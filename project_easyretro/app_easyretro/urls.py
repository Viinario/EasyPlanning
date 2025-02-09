from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FormViewSet, QuestionViewSet

router = DefaultRouter()
router.register(r'forms', FormViewSet)
router.register(r'questions', QuestionViewSet)

urlpatterns = [
    path('', include(router.urls)),
]