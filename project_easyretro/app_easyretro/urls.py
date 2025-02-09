from django.urls import path
from . import views

urlpatterns = [
    path('api/test/', views.api_test, name='api_test'),
    path('formulario/', views.create_formulario, name='create_formulario'),
    path('formulario/<id>/', views.get_formulario, name='get_formulario'),
]