from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),       # http://localhost:8000/
    path('formulario/', views.formulario, name='formulario'),
    path('listado/', views.listado, name='listado'),
]