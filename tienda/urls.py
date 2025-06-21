from django.urls import path
from . import views

urlpatterns = [
    path('landing/', views.landing, name='landing'),        # Página principal inventario
    path('formulario/', views.formulario, name='formulario'),  # Formulario para agregar producto
    path('listado/', views.listado, name='listado'),        # Página para editar producto
    path('', views.landing),  # Por defecto que la raíz vaya a landing
]