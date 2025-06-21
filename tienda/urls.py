from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),           # Página principal - inventario
    path('formulario/', views.formulario, name='formulario'),  # Formulario agregar producto
    path('listado/', views.listado, name='listado'),   # Listado de productos (opcional)
]
